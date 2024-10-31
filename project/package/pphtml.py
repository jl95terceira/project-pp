import re
import typing

from jl95terceira.pytools.pp import do_it, ProcessingInstruction

REGEX         = 'PPHTML'
SAFE_REGEX    = f'{REGEX}98006097C52D49A0961609C7E687AF2B'
BODY          = lambda r: f'{r}'
TAIL          = lambda r: f'{r}:TAIL'
COMMENT_BEGIN = '<!--'
COMMENT_END   = '-->'

def do_it(fn:str):

    do_it(fn =fn,
          pis=[ProcessingInstruction(abort_if=lambda fcontent,_a=abort_if_match_safe_rex: ((lambda m:     m) if _a else \
                                                                                           (lambda m: not m))(re.match(pattern=f'.*{SAFE_REGEX}.*',string=fcontent)),
                                     pattern =f'{re.escape(COMMENT_BEGIN)} *{BODY(rex)}(.*?){re.escape(COMMENT_END)}.*?{re.escape(COMMENT_BEGIN)} *{TAIL(rex)} *{re.escape(COMMENT_END)}',
                                     capture =lambda match                              : match.group(1),
                                     descape =lambda input                              : input.replace(COMMENT_END[:-1]+'\\'+COMMENT_END[-1], COMMENT_END),
                                     repl    =lambda output,match,rex=rex               : f'{COMMENT_BEGIN} {BODY(rex)}{match.group(1)}{COMMENT_END}\n{output}{COMMENT_BEGIN} {TAIL(rex)} {COMMENT_END}') for abort_if_match_safe_rex,rex in [(True,  REGEX), 
                                                                                                                                                                                                                                              (False, SAFE_REGEX)]])
    
if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(description='pre-processor for HTML files')
    p.add_argument('f',
                   help='file name')
    args = p.parse_args()
    do_it(fn=args.f)
