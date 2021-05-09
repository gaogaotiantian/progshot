import './App.css';
import {useEffect, useState} from 'react'
import Source from './components/Source'
import Terminal from './components/Terminal'

function App() {
  const [currSource, setCurrSource] = useState("")

  useEffect(() => {
    const getSource = async () => {
      const sourceCodeFromServer = await fetchSource()
      setCurrSource(sourceCodeFromServer)
    }
    getSource()
  }, [])

  const fetchSource = async () => {
    const res = await fetch('http://localhost:8080/')
    const data = await res.json()
    return data
  }

  const executeCommand = async (c) => {
    var url = new URL('http://localhost:8080/command')
    var params = {command: c.toString()}
    url.search = new URLSearchParams(params).toString();
    const res = await fetch(url)
    const data = await res.json()
    console.log(data)
    setCurrSource(data.source)
    return data.console
  }

  return (
    <div className="App">
      <div className="btn-group">
        <button>Up</button>
        <button>Down</button>
        <button>Next</button>
        <button>Back</button>
        <button>Where</button>
      </div>
      <div className="row">
        <Source currSource={currSource}/>
        <Terminal exeCommand={executeCommand}/>
      </div>
    </div>
  );
}

export default App;
