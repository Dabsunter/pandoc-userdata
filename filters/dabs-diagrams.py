#!/usr/bin/env python3

from panflute import *
import pandocfilters as pf

FILTER_NAME = "dabs-diagrams"

def render_mermaid(elem, doc):
    if type(elem) == pf.CodeBlock:
        if 'mermaid' in elem.classes:
            filename = pf.get_filename4code(
                FILTER_NAME,
                elem.text,
                'pdf' if doc.format == 'latex' else 'svg'
            )

            shell(f"""mmdc
                --output {filename}
                --pdfFit
                --puppeteerConfigFile ~/puppeteer-config.json""",
                msg=elem.text)
            
            return Image(
                url=filename,
                title=elem.attribute['caption'],
                classes=elem.classes,
                attributes=elem.attributes
            )
            


def main(doc=None):
    return run_filter(render_mermaid, doc=doc)

if __name__ == "__main__":
    main()