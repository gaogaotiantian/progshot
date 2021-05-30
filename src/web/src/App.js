import 'react-reflex/styles.css'
import {
  ReflexContainer,
  ReflexSplitter,
  ReflexElement
} from 'react-reflex'
import './App.css';
import {useState} from 'react'
import Source from './components/Source'
import Terminal from './components/Terminal'
import Variables from './components/Variables'
import Stack from './components/Stack'

const client = new WebSocket('ws://localhost:8080')

function App() {
  const [currSource, setCurrSource] = useState({
    code: "",
    curr_lineno: 0,
    locals: "",
    film: {
      name: "",
      num_films: 0,
      curr_film_idx: 0
    }
  })
  const [currFilm, setCurrFilm] = useState(0)
  const [stack, setStack] = useState({
    stack: [], 
    curr: 1
  })
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
      setCurrFilm(dataFromServer.source.film.curr_film_idx + 1)
    }
    if (dataFromServer.hasOwnProperty("console")) {
      addToConsoleHistory(dataFromServer.console, true)
    }
    if (dataFromServer.hasOwnProperty("stack")) {
      setStack(dataFromServer.stack)
    }
  }

  const sendCommand = async (c, type) => {
    var message 
    message = {"type": type,
                "command": c.toString()}
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
  }

  return (
    <div className="App">
      <ReflexContainer className="container" orientation="vertical">
        <ReflexElement>
          <ReflexContainer orientation="horizontal">
            <ReflexElement flex={0.6}>
              <Source currSource={currSource} currFilm={currFilm} setCurrFilm={setCurrFilm} sendCommand={sendCommand}/>
            </ReflexElement>
            <ReflexSplitter/>
            <ReflexElement>
              <Terminal sendCommand={sendCommand} addToConsoleHistory={addToConsoleHistory}
                        consoleHistory={consoleHistory} consoleOutputLines={consoleOutputLines}/>
            </ReflexElement>
          </ReflexContainer>
        </ReflexElement>

      <ReflexSplitter/>

        <ReflexElement>
          <ReflexContainer orientation="horizontal">
            <ReflexElement flex={0.5} className="stack">
              <Stack stack={stack} sendCommand={sendCommand}/>
            </ReflexElement>
            <ReflexSplitter/>
            <ReflexElement>
              <Variables currSource={currSource}/>
            </ReflexElement>
          </ReflexContainer>
        </ReflexElement>

      </ReflexContainer>
    </div>
  );
}

export default App;
