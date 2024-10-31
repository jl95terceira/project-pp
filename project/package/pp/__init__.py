import abc
import dataclasses
import os
import os.path
import re
import sys
import typing

class Writer(abc.ABC):

    @abc.abstractmethod
    def write     (self,part:str) -> None: pass

    def writeline (self,line:str):
        
        self.write(f'{line}\n')

    def writelines(self,lines:list[str]) -> None: 
        
        for line in lines:

            self.writeline(line)

class BufferWriter(Writer):

    def __init__(self):

        self._parts:list[str] = []
        self._whole:str       = ''

    @typing.override
    def write(self,part:str):

        self._parts.append(part)

    def build(self):

        if self._parts:

            self._whole = ''.join((self._whole, *self._parts,))
            self._parts.clear()
            
        return self._whole

@dataclasses.dataclass
class ProcessingInstruction:

    abort_if:typing.Callable[[str],bool]
    pattern :str
    capture :typing.Callable[[re.Match],str]
    descape :typing.Callable[[str],str]
    repl    :typing.Callable[[str],bool]

    def __post_init__(self):

        if self.abort_if is None: 
           self.abort_if = lambda fcontent: False

def do_it(fn :str,
          pis:typing.Iterable[ProcessingInstruction],
          enc:str='utf-8'):

    with open(fn, mode='r', encoding=enc) as f:

        original = f.read()
    
    def generated(expr:str) -> str:

        pp = BufferWriter()
        owd = os.getcwd()
        os.chdir(os.path.join(*(os.path.split(os.path.abspath(fn))[:-1])))
        try:

            sys.path.append(os.getcwd())
            exec(expr.replace('\\/', '/'), {
                
                **globals(),
                'write'     :pp.write,
                'writeline' :pp.writeline,
                'writelines':pp.writelines,
            
            })
            sys.path.pop()
        
        finally:

            os.chdir(owd)
        
        return pp.build()

    pprocessed = original
    pis_done:list[ProcessingInstruction] = list()
    for pi in pis:

        if pi.abort_if(original): 
            
            continue

        def replf(m:re.Match[str]):

            return (lambda input: pi.repl(generated(pi.descape(input)),m))(pi.capture(m))

        pprocessed = re.sub(pattern=pi.pattern, 
                            repl   =replf, 
                            string =pprocessed, 
                            flags  =re.DOTALL)
        pis_done.append(pi)

    with open(fn, mode='w', encoding=enc) as f:

        f.write(pprocessed)
    
    return pis_done
