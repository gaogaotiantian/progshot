import Prism from "prismjs"
import { useEffect } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'

Prism.manual = true;
const Stack = ({stack}) => {
    useEffect(() => {
        Prism.highlightAll();
    })

    return (
        <pre className="stack">
           <code className="language-py">{stack}</code>
        </pre>
    )
}

export default Stack; 