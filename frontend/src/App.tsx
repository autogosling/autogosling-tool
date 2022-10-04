import React, { useState } from 'react';
import logo from './logo.svg';
import { VIZ_BACKEND_URL } from './Config';
import './App.css';

function DataResult({ data } : {data : any}) {
  const { image, ...rest } = data
  return (
    <div>
      <h3>Viz Analysis Results</h3>
      <img src={image} />
      <pre>{JSON.stringify(rest, null, 2)}</pre>

    </div>)
}
function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const handleSubmit = async (e: any) => {
    e.preventDefault()
    const formObject = new FormData(e.currentTarget)
    alert("submitting!")
    const response = await fetch(VIZ_BACKEND_URL, {
      method: "POST",
      body: formObject
    })
    setError(!response.ok)
    const json = response.ok ? await response.json() : null
    setHasData(true)
    setData(json)
  }
  return (
    <div className="App">
      <h1>Autogosling Frontend</h1>
      <p>Upload your image here:</p>
      <form onSubmit={handleSubmit}>
        <input type="file" name="image" id="image" />
        <button type="submit">Submit image</button>
      </form>
      <br />
      {(hasData && !error) && <DataResult data={data} />}
    </div>
  );
}

export default App;
