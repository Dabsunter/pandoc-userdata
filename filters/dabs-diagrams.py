#!/usr/bin/env python3

from panflute import *
from pandocfilters import get_filename4code, get_extension
import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

FILTER_NAME = "dabs-diagrams"

def render_mermaid(elem, doc):
    if type(elem) == CodeBlock and 'mermaid' in elem.classes:
        outputname = get_filename4code(
            FILTER_NAME,
            elem.text,
            get_extension(doc.format, 'png', latex='pdf', html='svg')
        )

        if not os.path.isfile(outputname):
            shell(
                [
                    "mmdc",
                    # "--input", inputname,
                    "--output", outputname,
                    "--pupeteerConfig", "~/pupeteer-config.json"
                    "--pdfFit"
                ],
                msg=elem.text.encode('utf8')
            )

            # eprint("response", res)
            
        return Para(Image(
            *convert_text(elem.attributes['caption'])[0].content if 'caption' in elem.attributes else [],
            url=outputname,
            title='fig:' if 'caption' in elem.attributes else '',
            classes=elem.classes,
            attributes=elem.attributes
        ))
            


def main(doc=None):
    return run_filter(render_mermaid, doc=doc)

if __name__ == "__main__":
    main()

