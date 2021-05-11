import './App.css';
import {useState} from 'react'
import Source from './components/Source'
import Terminal from './components/Terminal'
import Variables from './components/Variables'
import Stack from './components/Stack'

const client = new WebSocket('ws://localhost:8080')

function App() {
  const [currSource, setCurrSource] = useState("")
  const [stack, setStack] = useState("")
  const [consoleHistory, setConsoleHistory] = useState("\n")
  const [consoleOutputLines, setConsoleOutputLines] = useState("1")
  const [consoleLineCount, setConsoleLineCount] = useState(1)

  client.onopen = () => {
    client.send(JSON.stringify({
      "type": "init",
    }))
  }

  client.onmessage = (message) => {
    const dataFromServer = JSON.parse(message.data);
    if (dataFromServer.hasOwnProperty("source")) {
      setCurrSource(dataFromServer.source)
    }
    if (dataFromServer.hasOwnProperty("console")) {
      addToConsoleHistory(dataFromServer.console, true)
    }
    if (dataFromServer.hasOwnProperty("stack")) {
      setStack(dataFromServer.stack)
    }
  }

  const sendCommand = async (c, isConsole) => {
    var message 
    if (isConsole) {
      message = {"type": "console",
                 "command": c.toString()}
    } else {
      message = {"type": "command",
                 "command": c.toString()}
    }
    client.send(JSON.stringify(message))
  }

  const addToConsoleHistory = (s, isOutput) => {
    var append = s
    if (isOutput) {
      calculateOutputLines(append)
    }
    setConsoleHistory(consoleHistory + append)
    setConsoleLineCount(consoleLineCount + (append.match(/\n/g) || []).length)
  }

  const calculateOutputLines = (output) => {
      const start = consoleLineCount + 1
      const end = consoleLineCount + (output.match(/\n/g) || []).length
      setConsoleOutputLines(consoleOutputLines + "," + start.toString() + "-" + end.toString())
      console.log(consoleOutputLines)
  }

  return (
    <div className="App">
      <div className="btn-group">
        <button onClick={() => sendCommand("up", false)}>Up</button>
        <button onClick={() => sendCommand("down", false)}>Down</button>
        <button onClick={() => sendCommand("next", false)}>Next</button>
        <button onClick={() => sendCommand("back", false)}>Back</button>
      </div>
      <div className="grid-container">
        <Source currSource={currSource}/>
        <Stack stack={stack}/>
        <Terminal sendCommand={sendCommand} addToConsoleHistory={addToConsoleHistory}
                  consoleHistory={consoleHistory} consoleOutputLines={consoleOutputLines}/>
        <Variables currSource={currSource}/>
      </div>
    </div>
  );
}

export default App;
