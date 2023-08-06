/*
 * LX-Tokenizer
 *
 */

%{

#include <locale.h>
#include <argp.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include "avlt.h"

#define localeString	"UTF-8"

/*
 * Behavior flags
 * - detachClitics: Detach clitics from verbs.
 * - expandContractions: Expand contracted forms (except those that are
 *   ambiguous with an uncontracted form).
 * - markClitics: Mark detached clitics with '-'.
 * - markExpansions: Mark the first element of an expanded contraction
 *   with '_'.
 * - markSpacing: Mark punctuation tokens with information about adjoinig
 *   spacing.
 * TODO:
 * - Use bit flags instead of unsigned char
 */
static unsigned char detachClitics = 1;
static unsigned char expandContractions = 1;
static unsigned char markClitics = 1;
static unsigned char markExpansions = 1;
static unsigned char markSpacing = 1;

// Key-Value node structure
typedef struct tree_Node {
	char *key;
	char *value;
} tree_Node;
typedef tree_Node *tree_NodePtr;

// The lists/trees 
static avlt_tree *abbrevTree;
static avlt_tree *cliticTree;
static avlt_tree *contrTree;

// Context flags 
static unsigned char foundBlank = 0;

// Spacing markers
const char *spaceL = "\\*";
const char *spaceR = "*/";

// Headers for functions defined below
tree_NodePtr searchTree(avlt_tree*,char*);
int countchr(char*,int);

%}

 // Parser states
%x tokenizing
%x abbrevFile
%x cliticFile
%x contrFile

 // Generic patterns
newline  "\n"|"\r\f"
 // spaces   [[:space:]]+
spaces [ \t]+
entity   "&"[[:alnum:]]+";"
xmlTag   "<"[^>]+">"
 
 // Patterns to parse the lists
comment  ^"%%".*{newline}
delim    "_"
inflec   "#"[[:alpha:]]+
tag      {delim}[[:alpha:]]+{inflec}?
header   ^{delim}.+{newline}
abbrev   ([:alpha:]|-|.|º|ª)+
clitic   [^% ,;\n\r\f]+
contr    [^%,;\n\r\f]+

 // Patterns for tokenization
digit    [0-9]
arabNum  {digit}+
ordinal  {arabNum}(º|ª)
punct    [[:punct:]]|«|»|"..."|"(...)"|"[...]"
word     [^[:punct:]\n[:space:]]+

emailUser    [[:alnum:]._-]+
domain       [[:alnum:]_-]+("."[[:alnum:]_-]+)+
emailAddress {emailUser}"@"{domain}
protocol     [[:alpha:]]+"://"
url          {protocol}?{domain}("/"[[:alnum:]._-~&=?;,]+)*"/"?
eaddress     {emailAddress}|{url}
acronym      [A-Z]("."[A-Z])*"."?
possessive   {word}"'s"

%%


<abbrevFile,cliticFile,contrFile>{comment}|{spaces}

<abbrevFile,cliticFile>{header} 

<abbrevFile>^.+$ {
        /*<abbrevFile>^{abbrev}$ {*/
	tree_NodePtr newNodePtr, result;
	char *word = strdup(yytext);
	newNodePtr = malloc(sizeof(tree_Node));
	newNodePtr->key = word;
	newNodePtr->value = NULL;
	result = avlt_insert(abbrevTree,newNodePtr);
	if (NULL != result) {
		fprintf(stderr,"ERROR : The abbreviation \"%s\" already exists\n",newNodePtr->key);
	}
}

<cliticFile>^{clitic}","{newline}{clitic}" "{clitic}";"{newline}{clitic}{tag}" "{clitic}{tag}$ {
	tree_NodePtr newNodePtr, result;

	char *cont, *expansion;
	cont = strtok(yytext,",");
	expansion = strtok(NULL,";");
	newNodePtr = malloc(sizeof(tree_Node));
	newNodePtr->key = strdup(cont);
	newNodePtr->value = strdup(expansion+1);
	result = avlt_insert(cliticTree,newNodePtr);
	if (NULL != result) {
		fprintf(stderr,"ERROR : The clitic/ending \"%s\" already exists\n",newNodePtr->key);
	}
}

<cliticFile>^"/"{clitic}$ {
	tree_NodePtr newNodePtr, result;
	newNodePtr = malloc(sizeof(tree_Node));
	newNodePtr->key = strdup(yytext+1);
	newNodePtr->value = "/";
	result = avlt_insert(cliticTree,newNodePtr);
	if (NULL != result) {
		fprintf(stderr,"ERROR : The clitic/ending \"%s\" already exists\n",newNodePtr->key);
	}
}

<cliticFile>^{clitic}$ {
	tree_NodePtr newNodePtr, result;
	char *word = strdup(yytext);
	newNodePtr = malloc(sizeof(tree_Node));
	newNodePtr->key = word;
	newNodePtr->value = NULL;
	result = avlt_insert(cliticTree,newNodePtr);
	if (NULL != result) {
		fprintf(stderr,"ERROR : The clitic/ending \"%s\" already exists\n",newNodePtr->key);
	}
}

<contrFile>^{contr}","{newline}{contr}(" "{contr})?";"{newline}{contr}{tag}(" "{contr}{tag})?"."$ {
	tree_NodePtr newNodePtr, result;
	char *cont, *expansion;
	cont = strtok(yytext,",");
	expansion = strtok(NULL,";");
	newNodePtr = malloc(sizeof(tree_Node));
	newNodePtr->key = strdup(cont);
	newNodePtr->value = strdup(expansion+1);
	result = avlt_insert(contrTree,newNodePtr);
	if (NULL != result) {
		fprintf(stderr,"ERROR : The contraction \"%s\" already exists\n",newNodePtr->key);
	}
}

<abbrevFile,cliticFile,contrFile>.|{newline}

<tokenizing>{newline} {
 	fprintf(stdout, "%s", yytext);
 	fflush(stdout);
    foundBlank = 1;
}

<tokenizing>{spaces} {
	fprintf(stdout, "%s", yytext);
    foundBlank = 1;
}

<tokenizing>{xmlTag}|{entity} {
  ECHO;
}

<tokenizing>{arabNum}|{ordinal}|{eaddress}|{acronym}|{possessive} {
    fprintf(stdout, " %s ", yytext);
    foundBlank = 0;
}

<tokenizing>{word}"."(ª|º)? {
    tree_NodePtr result;

    if (NULL != (result = searchTree(abbrevTree,yytext))) {
      fprintf(stdout, " %s ", yytext);
    } else {
      REJECT;
      // The use of REJECT entails a performance penalty which, for a
      // tokenizer, may be noticeable. Maybe I should replace the else
      // branch by an explicit splitting of the match into two tokens.
    }
}

<tokenizing>{punct} {
    char nextChar;
	if (markSpacing) {
		nextChar = input();
		if (foundBlank) {
			if (isspace(nextChar)) {
				fprintf(stdout, " %s%s%s ", spaceL, yytext, spaceR);
			} else {
				fprintf(stdout, " %s%s ", spaceL, yytext);
			}
		} else {
			if (isspace(nextChar)) {
				fprintf(stdout, " %s%s ", yytext, spaceR);
			} else {
				fprintf(stdout, " %s ", yytext);
			}
		}
		unput(nextChar);
	} else {
		fprintf(stdout, " %s ", yytext);
	}
    foundBlank = 0;
}

<tokenizing>{word} {
	tree_NodePtr result;
    if ((expandContractions) && (NULL != (result = searchTree(contrTree,yytext)))) {
		// TODO: Expand taking into account the capitalization
	    char *spcIndx = strchr(result->value,' ');
		if (NULL != spcIndx) {
		    *spcIndx = '\0';
			fprintf(stdout, "%s%s %s", result->value, markExpansions?"_":"", spcIndx+1);
		    *spcIndx = ' ';
		} else {
			fprintf(stdout, "%s ", result->value);
		}
	} else {
		fprintf(stdout, "%s ", yytext);
	}
    foundBlank = 0;
}

<tokenizing>{word}("-"{word})+ {
    #define maskNormal  0x01 // 0000 0001
    #define maskContr   0x02 // 0000 0010
    #define maskEnding  0x04 // 0000 0100
    #define maskVocalic 0x08 // 0000 1000
    #define maskValid   0x80 // 1000 0000
	#define SET_NORMAL(x)  (x |= maskNormal)
	#define SET_CONTR(x)   (x |= maskContr)
	#define SET_ENDING(x)  (x |= maskEnding)
	#define SET_VOCALIC(x) (x |= maskVocalic)
	#define SET_VALID(x)   (x |= maskValid)
	#define UNSET_VALID(x) (x &= (~maskValid))
	#define FLAG_NORMAL(x)  (x & maskNormal)
	#define FLAG_CONTR(x)   (x & maskContr)
	#define FLAG_ENDING(x)  (x & maskEnding)
	#define FLAG_VOCALIC(x) (x & maskVocalic)
	#define FLAG_VALID(x)   (x & maskValid)
	#define MAX_ELEMENTS 4
	int nElements = countchr(yytext, '-');
	if ((detachClitics) && (nElements <= MAX_ELEMENTS)) {
		tree_NodePtr result;
		char *elemArray[MAX_ELEMENTS+1];
		char *workStr, *hyphPtr, *elemPtr;
		unsigned char arrayIndx;
		unsigned char flags = 0;
		
		// Get -parts of token
		arrayIndx = 0;
		elemPtr = workStr = strdup(yytext);
		elemArray[arrayIndx] = elemPtr;
		hyphPtr = strchr(elemPtr,'-');
		while (NULL != hyphPtr) {
			*hyphPtr = '\0';
			elemPtr = hyphPtr+1;
			arrayIndx++;
			elemArray[arrayIndx] = elemPtr;
			hyphPtr = strchr(elemPtr,'-');
		}
		for (arrayIndx=0; arrayIndx <= nElements; arrayIndx++) {
		    elemArray[arrayIndx] = strdup(elemArray[arrayIndx]);
		}

		// Verify format
		SET_VALID(flags);
		for (arrayIndx=1; arrayIndx <= nElements; arrayIndx++) {
            if (NULL != (result = searchTree(cliticTree,elemArray[arrayIndx]))) {
			    if (NULL == result->value) {
				    if (FLAG_ENDING(flags) || FLAG_CONTR(flags)) {
					    UNSET_VALID(flags);
					} else {
						SET_NORMAL(flags);
					}
				} else {
				    if ('/' == result->value[0]) {
					    if (FLAG_ENDING(flags) || (!(FLAG_NORMAL(flags) || FLAG_CONTR(flags)))) {
							UNSET_VALID(flags);
						} else {
							SET_ENDING(flags);
						}
					} else {
					    if (FLAG_ENDING(flags)) {
							UNSET_VALID(flags);
						} else {
							SET_CONTR(flags);
							free(elemArray[arrayIndx]);
							// TODO: Expand taking into account the capitalization
							if (markClitics) {
								char *spcPtr = strchr(result->value, ' ');
								unsigned char expLen = strlen(result->value);
								unsigned char fstLen = spcPtr-(result->value)+1;
								elemArray[arrayIndx] = (char*) malloc(expLen+2);
								strncpy(elemArray[arrayIndx],result->value,fstLen);
								elemArray[arrayIndx][fstLen] = '-';
								strncpy((elemArray[arrayIndx]+fstLen+1),spcPtr+1,expLen-fstLen);
								elemArray[arrayIndx][expLen+1] = '\0';
							} else {
								elemArray[arrayIndx] = strdup(result->value);
							}
						}
					}
				}
			} else {
				UNSET_VALID(flags);
			}
		}
		
		// Print token
		if (FLAG_VALID(flags)) {
		    if ((0 == strcasecmp(elemArray[1], "lo")) ||
			    (0 == strcasecmp(elemArray[1], "la")) ||
				(0 == strcasecmp(elemArray[1], "los")) ||
				(0 == strcasecmp(elemArray[1], "las"))) {
			    SET_VOCALIC(flags);
			}
			fprintf(stdout, "%s%s", elemArray[0], FLAG_VOCALIC(flags)?"#":"");
			if (FLAG_ENDING(flags)) {
				fprintf(stdout, "-CL-%s", elemArray[nElements]);
			}
			fprintf(stdout, " ");
			for (arrayIndx=1; arrayIndx <= (FLAG_ENDING(flags)?(nElements-1):nElements); arrayIndx++) {
				fprintf(stdout, "%s%s ", markClitics?"-":"", elemArray[arrayIndx]);
			}
		} else {
			fprintf(stdout, "%s ", yytext);
		}
		
		// Cleanup
		for (arrayIndx=0; arrayIndx <= nElements; arrayIndx++) {
		    free(elemArray[arrayIndx]);
		}
		free(workStr);

	} else {
		fprintf(stdout, "%s ", yytext);
	}
    foundBlank = 0;
}


%%


/*
 * Wrapper function to search the tree
 */
tree_NodePtr searchTree(avlt_tree *tree, char *key) {
	tree_Node dummy;
	void **data = NULL;
	dummy.key = key;
	data = avlt_find(tree,&dummy);
	if (NULL != data) {
		return (tree_NodePtr) *data;
	} else {
		return NULL;
	}
}


/*
 * Counts the number of occurrences of c in string
 */
int countchr(char *string, int c) {
    int count = 0;
    while (NULL != string) {
      string = strchr(string,c);
      if (string != NULL) {
        string++;
        count++;
      }
    }
    return count;
}


/*
 * Node comparison function
 * Takes each node and passes the strings in the key field to strcasecmp()
 *
 */
int normalStrComp(void *a, void *b, void *param) {
	tree_NodePtr x = a;
	tree_NodePtr y = b;
	return strcasecmp(y->key, x->key);
}


/*
 * Argp - Command line parser
 *
 */
const char *argp_program_version = "LX-Tokenizer 0.1";
const char *argp_program_bug_address = "<jsilva@di.fc.ul.pt>";
static char doc[] =
	"\nLX-Tokenizer\v"
	"Tokenizes a raw text.";
static char args_doc[] = "<Abbreviations> <Clitics> <Contractions>";
static struct argp_option options[] = {
	{"verbose", 'v', 0, 0, "Be verbose"},
	{0}
};
struct arguments {
	char *args[3];
	int verbose;
};
static error_t parse_opt(int key, char *arg, struct argp_state *state) {
	struct arguments *arguments = state->input;
	switch (key) {
	case 'v':
		arguments->verbose = 1;
		break;
	case ARGP_KEY_NO_ARGS:
		argp_usage(state);
	case ARGP_KEY_ARG:
		if (state->arg_num >= 3)
			argp_usage(state);
		arguments->args[state->arg_num] = arg;
		break;
	case ARGP_KEY_END:
		if (state->arg_num < 3)
			argp_usage(state);
		break;
	default:
		return ARGP_ERR_UNKNOWN;
	}
	return 0;
};
static struct argp argp = {options,parse_opt,args_doc,doc};


/*
 * Main
 *
 */
int main(int argc, char **argv) {
	char *fileErrorMsg = "Error while trying to open \"%s\"\n";
    FILE *abbrevFilePtr, *cliticFilePtr, *contrFilePtr;

	/*
	 * Parse the command line
	 */
	struct arguments arguments;
	arguments.verbose = 0;
	argp_parse(&argp,argc,argv,0,0,&arguments);
	
	/*
	 * Open the list files
	 */
	if (NULL == (abbrevFilePtr = fopen(arguments.args[0],"r"))) {
		fprintf(stderr,fileErrorMsg,arguments.args[0]);
		exit(1);
	}
	if (NULL == (cliticFilePtr = fopen(arguments.args[1],"r"))) {
		fprintf(stderr,fileErrorMsg,arguments.args[1]);
		exit(1);
	}
	if (NULL == (contrFilePtr = fopen(arguments.args[2],"r"))) {
		fprintf(stderr,fileErrorMsg,arguments.args[2]);
		exit(1);
	}
	
	/*
	 * Parse the abbreviation file
	 */
	BEGIN(abbrevFile);
	yyrestart(abbrevFilePtr);
	abbrevTree = avlt_create((avl_comparison_func)normalStrComp,NULL);
	if (arguments.verbose) {
		fprintf(stderr,"Parsing the abbreviation file...\n");
	}
	yylex();
	fclose(abbrevFilePtr);
	
	/*
	 * Parse the clitic file
	 */
	BEGIN(cliticFile);
	yyrestart(cliticFilePtr);
	cliticTree = avlt_create((avl_comparison_func)normalStrComp,NULL);
	if (arguments.verbose) {
		fprintf(stderr,"Parsing the clitic file...\n");
	}
	yylex();
	fclose(cliticFilePtr);
	
	/*
	 * Parse the contraction file
	 */
	BEGIN(contrFile);
	yyrestart(contrFilePtr);
	contrTree = avlt_create((avl_comparison_func)normalStrComp,NULL);
	if (arguments.verbose) {
		fprintf(stderr,"Parsing the contraction file...\n");
	}
	yylex();
	fclose(contrFilePtr);
	
	/*
	 * Start tokenizer
	 */
	BEGIN(tokenizing);
	yyrestart(stdin);
    yylex();
    return 0;
}
