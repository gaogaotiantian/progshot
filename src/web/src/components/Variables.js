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
        <div className="section">
            <div className="grid">
                <div className="section-title">Variables</div>
                <pre className="variables">
                    <code className="language-py">{currSource.locals}</code>
                </pre>
            </div>
        </div>
    )
}

export default Variables; 