import Prism from "prismjs"
import { useEffect } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'

Prism.manual = true;
const Variables = ({currSource}) => {
    useEffect(() => {
        Prism.highlightAll();
    })

    return (
        <pre className="variables">
           <code className="language-py">{currSource.locals}</code>
        </pre>
        // <pre>
        //     <code className="language-py"></code>
        // </pre>
    )
}

export default Variables; 