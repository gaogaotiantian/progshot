import Prism from "prismjs"
import { useEffect } from "react";
import '../App.css';
import "../prism.css";
import 'prismjs/components/prism-python'
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/plugins/line-highlight/prism-line-highlight'

Prism.manual = true;
const Source = ({currSource}) => {
    useEffect(() => {
        Prism.highlightAll();
    })

    console.log(currSource.code)
    return (
        <pre className="line-numbers column" data-line={currSource.curr_lineno}>
           <code className="language-py">{currSource.code}</code>
        </pre>
        // <pre>
        //     <code className="language-py"></code>
        // </pre>
    )
}

export default Source; 