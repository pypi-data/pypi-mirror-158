/*
 * Sentence Chunker (one-nl mode)
 */


%{

// If CHUNKER_DEBUG is defined, there will be no sentence chunking. Instead,
// a colored mark with the number of the applied rule will be output to
// signal the chunker's decisions:
//  RED   : chunks
//  GREEN : doesn't chunk (fake separator)

//#define CHUNKER_DEBUG	1

#include "string.h"
#include <locale.h>
#include <argp.h>

#define localeString	"UTF-8"

#ifdef CHUNKER_DEBUG
#define YY_USER_INIT	printf("[41m<BOF>[0m")
#define	CHUNK		printf("#[41m%d[0m",yy_act)
#define	NOT_CHUNK	printf("[42m%d[0m",yy_act)
#define END_OF_FILE	printf("[41m<EOF>[0m")
#else
#define YY_USER_INIT	printf("<p> <s> ")
#define	SENT_CHUNK	printf(" </s>\n<s> ")
#define CHUNK		if(('\n' == *yytext) || ('\r' == *yytext)){printf(" </s>\n</p>\n\n<p> <s> ");}else{SENT_CHUNK;}
#define	NOT_CHUNK	// No-Op
#define END_OF_FILE	printf(" </s>\n</p>\n\n")
#endif

%}


%x chunk_one_nl
%x subtract_from_chunking_one
%x chunk_one_chunk_again
%x chunk_one_beginning_turn_state
%x chunk_one_keeping_turn_state
%x chunk_one_retaking_turn_state


 // Syntactically valid roman numerals (all upper or all lower)
validRomanHiC	M*(CM|DC{0,3}|CD|C{1,3})(XC|LX{0,3}|XL|X{0,3})(IX|VI{0,3}|IV|I{0,3})
validRomanHiX	M*(CM|DC{0,3}|CD|C{0,3})(XC|LX{0,3}|XL|X{1,3})(IX|VI{0,3}|IV|I{0,3})
validRomanHiI	M*(CM|DC{0,3}|CD|C{0,3})(XC|LX{0,3}|XL|X{0,3})(IX|VI{0,3}|IV|I{1,3})
validRomanHi	{validRomanHiC}|{validRomanHiX}|{validRomanHiI}
validRomanLoC	m*(cm|dc{0,3}|cd|c{1,3})(xc|lx{0,3}|xl|x{0,3})(ix|vi{0,3}|iv|i{0,3})
validRomanLoX	m*(cm|dc{0,3}|cd|c{0,3})(xc|lx{0,3}|xl|x{1,3})(ix|vi{0,3}|iv|i{0,3})
validRomanLoI	m*(cm|dc{0,3}|cd|c{0,3})(xc|lx{0,3}|xl|x{0,3})(ix|vi{0,3}|iv|i{1,3})
validRomanLo	{validRomanLoC}|{validRomanLoX}|{validRomanLoI}
validRoman	{validRomanHi}|{validRomanLo}

 // Basic patterns: blanks and characters
blank		[ \t]
blank_or_nl	[ \t\v]|"\n"|"\r\n"
characterMin	[a-záàéèíìóòúùçâêôîûãõäëïöüÿ]
characterMax	[A-ZÁÀÉÈÍÌÓÒÚÙÇÂÊÔÎÛÃÕÄËÏÖÜ]
character	{characterMin}|{characterMax}
non_letter	[^a-záàéèíìóòúùçâêôîûãõäëïöüÿA-ZÁÀÉÈÍÌÓÒÚÙÇÂÊÔÎÛÃÕÄËÏÖÜ]

 // Sequence of blanks with AT LEAST one character and AT MOST one newline
b_nl_b		{blank}*{blank_or_nl}{blank}*

 // A hyphen must have characters to it's left or right, otherwise it's
 // considered not to be a hyphen but a dialogue marker
actual_hyphen	"-"({character}|[0-9])|({character}|[0-9])"-"

 // Patterns that are allowed in a parenthetical sentence
chars_btw_dashes	({actual_hyphen}|[^-.?!])

 // A dash: "-", "--" or "---"
dash	"-"{1,3}

 // Proper names
pnm	{characterMax}{character}+

 // Initiators
ini_reg		{characterMax}|[0-9]|("..."|"(...)"|"[...]"){blank}
ini_pre_reg	['"«[(]+{ini_reg}
initiator	{ini_reg}|{ini_pre_reg}

ini_quote	['"«]{ini_reg}

 // Terminators
term_reg	"."|[?!]+|"..."|"..."[?!]+|[?!]+"..."|{blank}("(...)"|"[...]")
term_pos_reg	{term_reg}['"»\])]
terminator	{term_reg}|{term_pos_reg}

term_estrut	("\n"|"\r\n"){blank}*

term_pre_quote	":"

 // Pattern prefixes of abbreviations ending in '.' and entering a multi-word token
 // Capitalization regime allowed: all lower, first caps, all upper
 // These pattern prefixes are used to define full abbreviations in {fake_term_*} below
abbr_address_scaps	Av|Pr|Trav|Lt|Estr|Lrg|Rot
abbr_address_upper	R|AV|PR|TRAV|LT|ESTR|LRG|ROT
abbr_address		{abbr_address_scaps}|{abbr_address_upper}

abbr_eclesiastic_lower	pe|fr|ab
abbr_eclesiastic_scaps	Pe|Fr|Ab
abbr_eclesiastic_upper	S|PE|FR|AB
abbr_eclesiastic	{abbr_eclesiastic_lower}|{abbr_eclesiastic_scaps}|{abbr_eclesiastic_upper}

abbr_excelence_lower	ex(º|ª|o|a|s|os|as|cia|ciª|cias|ca|cas|cª|mo|mº|mos|ma|mª|mas)?
abbr_excelence_scaps	Ex(º|ª|o|a|s|os|as|cia|ciª|cias|ca|cas|cª|mo|mº|mos|ma|mª|mas)?
abbr_excelence_upper	EX(º|ª|O|A|S|OS|AS|CIA|CIª|CIAS|CA|CAS|Cª|MO|Mº|MOS|MA|Mª|MAS)?
abbr_excelence		{abbr_excelence_lower}|{abbr_excelence_scaps}|{abbr_excelence_upper}

abbr_function_lower	pres|sec[ºª]?|sub-sec[ºª]?|dirª?
abbr_function_scaps	Pres|Sec[ºª]?|Sub-sec[ºª]?|Dirª?
abbr_function_upper	PRES|SEC[ºª]?|SUB-SEC[ºª]?|DIRª?
abbr_function		{abbr_function_lower}|{abbr_function_scaps}|{abbr_function_upper}

abbr_professional_lower	dr[aª]?|eng[ºaª]?|prof[aª]?|arq[ºaªu]?
abbr_professional_scaps	Dr[aª]?|Eng[ºaª]?|Prof[aª]?|Arq[ºaªu]?
abbr_professional_upper	DR[Aª]?|ENG[ºAª]?|PROF[Aª]?|ARQ[ºAªU]?
abbr_professional	{abbr_professional_lower}|{abbr_professional_scaps}|{abbr_professional_upper}

abbr_treatment_lower	s(r|rs|nr|ra|nra|rª|nrª)
abbr_treatment_scaps	S(r|rs|nr|ra|nra|rª|nrª)
abbr_treatment_upper	D|S(R|RS|NR|RA|NRA|Rª|NRª)
abbr_treatment		{abbr_treatment_lower}|{abbr_treatment_scaps}|{abbr_treatment_upper}

abbr_yours_something_lower	s"."{blank}+(rev|revª|revma|revmª|a|em|emª|ex|exª|exa|mag|maga|m|s|sª|pat)|s.{blank}+ex.{blank}+rev|s.{blank}+exª.{blank}+revª
abbr_yours_something_scaps	S"."{blank}+(Rev|Revª|Revma|Revmª|A|Em|Emª|Ex|Exª|Exa|Mag|Maga|M|S|Sª|Pat)|S.{blank}+Ex.{blank}+Rev|S.{blank}+Exª.{blank}+Revª
abbr_yours_something_upper	S"."{blank}+(REV|REVª|REVMA|REVMª|A|EM|EMª|EX|EXª|EXA|MAG|MAGA|M|S|Sª|PAT)|S.{blank}+EX.{blank}+REV|S.{blank}+EXª.{blank}+REVª
abbr_yours_something		{abbr_yours_something_lower}|{abbr_yours_something_scaps}|{abbr_yours_something_upper}

 // Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation is a proper name
 // The corresponding '.' is a fake terminator
fake_term_pre_PNM	({abbr_treatment}|{abbr_function}|{abbr_eclesiastic}|{abbr_professional}|{abbr_excelence}|{abbr_yours_something})"."

 // Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation is a numeral (arab or roman)
 // The corresponding '.' is a fake terminator
fake_term_pre_digit_lower	seg|qua|qui|sex|sáb|jan|fev|abr|mai|jun|jul|ago|out|nov|no|n|num|cap|ex|fig|fl|pg|pág|pgs|págs|sec|séc|tab|vol
fake_term_pre_digit_scaps	Seg|Qua|Qui|Sex|Sáb|Jan|Fev|Abr|Mai|Jun|Jul|Ago|Out|Nov|No|Num|Cap|Ex|Fig|Fl|Pg|Pág|Pgs|Págs|Sec|Séc|Tab|Vol
fake_term_pre_digit_upper	SEG|QUA|QUI|SEX|SÁB|JAN|FEV|ABR|MAI|JUN|JUL|AGO|OUT|NOV|NO|N|NUM|CAP|EX|FIG|FL|PG|PÁG|PGS|PÁGS|SEC|SÉC|TAB|VOL
fake_term_pre_digit		({fake_term_pre_digit_lower}|{fake_term_pre_digit_scaps}|{fake_term_pre_digit_upper})"."

 // Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation is of any type
 // The corresponding '.' is a fake terminator
 // Note: the [A...Ü] in the pattern below is like {characterMax}, but excludes "É" (verb) and "Ã" (possibly an interjection)
fake_term_always_lower	"v."|"i.e."|"vs."|"cf."|"e.g."
fake_term_always_upper	"I.E."|"VS."|"CF."|"E.G."|[A-ZÁÀÈÍÌÓÒÚÙÇÂÊÔÎÛÕÄËÏÖÜ]"."

fake_term_always	{fake_term_always_lower}|{fake_term_always_upper}|{abbr_address}"."

 // Pattern that precedes abbreviations 
 // Used in rules below to prevent endings of words that immediately precede '.' to be taken as abbreviations
token_separator		{blank}|['"«[(]|"-"{blank}

 // Header of an enumeration
enum_header	([0-9]{1,2}|{validRoman})[.)]|"("([0-9]{1,2}|{validRoman})")"|{characterMin}")"|"("{characterMin}")"


	// REMINDER
	// Tokens ambiguous between abbreviation (ex.: ter./terça-feira) and word followed by '.' (ter_V ._PNT)
	// These tokens are not in the lists of abbreviations above
	// At its present version, the chunker always interprets the '.' here as a true terminator sign
	/* ter. dom. mar. set. dez. par.  */
	// REMINDER
	// The last '.' in an acronym may be ambivalent between marking the end of the acronym and the end of a
	// sentence.
	// At its present version the chunker always interprets the '.' here only as a terminator of the
	// acronym, never chunking at this point.
	// REMINDER
	// The last '.' in an abbreviation may be ambivalent between marking the end of the abbreviation and the end
	// of a sentence.
	// At its present version the chunker always interprets the '.' here both as a terminator of the
	// abbreviation and of the sentence, always chunking at this point when the abbreviation is not listed in the
	// patterns defined above.


%%


<chunk_one_nl>{
({term_estrut}{blank}*|{term_pre_quote}{blank_or_nl})/{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+ {
	// **** DIALOGUE MARKING ****
	// Rule 1
	// Beginning of a turn of a speaker, followed by narrator's comment
	// The comment is chunked by Rules .../... or skipped by Rule ...
	ECHO; CHUNK; BEGIN(chunk_one_beginning_turn_state);
}
({term_estrut}{blank}*|{term_pre_quote}{blank_or_nl})/{dash}{blank}+{initiator}	{
	// Rule 2
	// Beginning of a turn of a speaker
	ECHO; CHUNK; BEGIN(chunk_one_beginning_turn_state);
}
{term_reg}{blank}+/{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+ {
	// Rule 3
	// Utterance immediately following previous utterance, followed by narrator's comment
	// The comment is chunked by Rules .../... or skipped by Rule ...
	ECHO; CHUNK; BEGIN(chunk_one_keeping_turn_state);
}
{term_reg}{blank}+/{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+ {
	// Rule 4
	// Utterance following narrator's comment, and followed by narrator's comment
	// The comment is chunked by Rules .../... or skipped by Rule ...
	ECHO; CHUNK; BEGIN(chunk_one_retaking_turn_state);
}
{term_reg}{blank}+/{dash}{blank}+{ini_reg} {
	// Rule 5
	// Utterance following narrator's comment
	ECHO; CHUNK;
}
":"{blank}+/{enum_header}{blank}+{initiator}[^;.?!]*{terminator}	{
	// **** HEADERS OF ENUMERATIONS ****
	// Rule 6
	// Beginning of list of enumerated sentences
	// It might be an enumeration in a single sentence, following a ":", but there's no ";" up to the first {terminator}
	// The sentence header is skipped by Rule ...
	// The {initiator} is skipped if it is "..." by Rule ...
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
[:;]{blank}+{enum_header}/{blank}+{initiator}	{
	// Rule 7
	// Boundary between a term and the next in an enumeration in a single sentence
	NOT_CHUNK; ECHO;
}
({term_estrut}{blank}*|{terminator}{blank}+)/{enum_header}{blank}+{initiator}	{
	// Rule 8
	// Header of sentence in list of enumerated sentences
	// The endings of the header (e.g. '.', ')', etc) are fake sentence terminators
	// The sentence header is skipped by Rule ...
	// The {initiator} is skipped if it is "..." by Rule ...
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
^{fake_term_pre_PNM}/{blank}+{pnm}			|
{token_separator}{fake_term_pre_PNM}/{blank}+{pnm}	{
	// **** ABBREVIATIONS ****
	// Rules 9-10
 	// Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation is a proper name
 	// The corresponding '.' is a fake terminator
	NOT_CHUNK; ECHO;
}
^{fake_term_always}/{blank}			|
{token_separator}{fake_term_always}/{blank}	{
	// Rules 11-12
 	// Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation can be of any type
 	// The corresponding '.' is a fake terminator
	NOT_CHUNK; ECHO;
}
^{fake_term_pre_digit}/{blank}*[0-9]+					|
{token_separator}{fake_term_pre_digit}/{blank}*[0-9]+			|
^{fake_term_pre_digit}/{blank}*{validRoman}{non_letter}			|
{token_separator}{fake_term_pre_digit}/{blank}*{validRoman}{non_letter}	{
	// Rules 13-16
 	// Abbreviations ending in '.' and entering a multi-word token: the token following the abbreviation is a numeral (arab or roman)
	// A roman numeral must be followed by a non-letter to assure it's not a prefix of a word
 	// The corresponding '.' is a fake terminator
	NOT_CHUNK; ECHO;
}
({characterMax}"."){2,}/{blank}	{
	// Rules 17
	// Acronyms
	// To be accepted as an acronym, it must have AT LEAST two "elements"
 	// The last '.' in the acronym is a fake terminator
	NOT_CHUNK; ECHO;
}
{terminator}{blank}+/({initiator}|{enum_header})	{
	// **** GENERAL, WELL BEHAVED SENTENCE CASES ****
	// Rule 18
	// Sentence (and possibly paragraph) separator
	ECHO; CHUNK;
}
{term_estrut}{blank}*/({initiator}|{enum_header})	{
	// **** GENERAL, WELL BEHAVED PARAGRAPH CASES ****
	// Rule 19
	// Begining of paragraph/header
	ECHO; CHUNK;
}
{terminator}{blank_or_nl}+/"..."{blank}+({initiator}|{enum_header})	{
	// **** AMBIGUOUS TERMINATORS/INITIATORS
	// Rule 20
	// The '...' is skipped by Rule ...
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
({term_estrut}{blank}*|{terminator}{blank_or_nl}+)/("(...)"|"[...]"){blank_or_nl}+({initiator}|{enum_header})	{
	// Rule 21
	// Beginning of sentence-ellipsis
	// The end of sentence-ellipsis is chunked by Rule ...
	ECHO; CHUNK; BEGIN(chunk_one_chunk_again);
}
{term_pre_quote}{blank_or_nl}+/{ini_quote}	{
	// **** QUOTATION ****
	// Rule 22
	// Beginning of indirect speech or "major" quotation
	// Allow several newlines between the ':' and the beginning of the quotation?
	ECHO; CHUNK;
}
}

<chunk_one_chunk_again>{
("(...)"|"[...]"){blank_or_nl}+	{
	// Rule 23
	// End sentence-ellipsis
	ECHO; CHUNK; BEGIN(chunk_one_nl);
}
}

<subtract_from_chunking_one>{
"..."	{
	// Rule 24
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
{dash}{blank}+"..."	{
	// Rule 25
	// Skips "hesitations" in the beginning of dialogue
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
{enum_header}{blank}+"..."	{
	// Rule 26
	// Skips the sentence header
	// Also skips the "..." to avoid it being erroneously taken as terminator
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
{enum_header}	{
	// Rule 27
	// Skips the sentence header
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
}

<chunk_one_beginning_turn_state>{
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/"..."	{
	// Rule 28
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/{ini_reg}	{
	// Rule 29
	ECHO; CHUNK; BEGIN(chunk_one_nl);
}
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}	{
	// Rule 30
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
{dash}{blank}+"..."	{
	// Rule 31
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
{dash}	{
	// Rule 32
	NOT_CHUNK; yyless(0); BEGIN(chunk_one_nl);
}
}

<chunk_one_keeping_turn_state>{
{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/"..."	{
	// Rule 33
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/{ini_reg}	{
	// Rule 34
	ECHO; CHUNK; BEGIN(chunk_one_nl);
}
{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}	{
	// Rule 35
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
}

<chunk_one_retaking_turn_state>{
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/"..."	{
	// Rule 36
	ECHO; CHUNK; BEGIN(subtract_from_chunking_one);
}
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}+/{ini_reg}	{
	// Rule 37
	ECHO; CHUNK; BEGIN(chunk_one_nl);
}
{dash}{blank}+{initiator}{chars_btw_dashes}*{term_reg}{blank}+{dash}{blank}	{
	// Rule 38
	NOT_CHUNK; ECHO; BEGIN(chunk_one_nl);
}
}


<<EOF>>	{
	// Reached the end of the file
	END_OF_FILE; yyterminate();
}


%%

int main() {
/*
	// The is "LX-Chunker: part of the LX-Suite of tools\n(c) 2002 A. Branco and J. Silva" (73 characters).
	// The message is Sequential-XOR encoded in the string below. The ASCII codes are in octal (see "man ascii").
	char *message = "\114\24\71\172\22\147\11\142\7\165\117\157\37\176\14\170\130\67\121\161\5\155\10\50\144\74\21\102\67\136\52\117\157\0\146\106\62\135\62\136\55\47\17\154\105\145\127\147\127\145\105\4\52\12\110\72\133\65\126\71\31\170\26\162\122\30\66\26\105\54\100\66\127";
	char letter;
	int i, msgLen;
	// Hard-coded length because the string has a \0 character, preventing strlen() from returning the correct value.
	msgLen = 73;
	// Sequential-XOR
	letter = message[0];
        fputc(letter, stderr);
        for (i = 1; i < msgLen; i++) {
                letter = message[i-1]^message[i];
                fputc(letter, stderr);
        }
        fputc('\n', stderr);
	*/
	BEGIN(chunk_one_nl);
	yylex();

	return 0;
}

