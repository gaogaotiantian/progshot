import Prism from "prismjs"
import { useEffect, useRef } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'

Prism.manual = true;
const Variables = ({currSource}) => {
    const variables = useRef(null);

    useEffect(() => {
        Prism.highlightAllUnder(variables.current);
    })

    return (
        <div className="section">
            <div className="section-title">Variables</div>
            <div className="scrollable">
                <pre className="variables" ref={variables}>
                    <code className="language-py">{currSource.locals}</code>
                </pre>
            </div>
        </div>
    )
}

export default Variables; 
