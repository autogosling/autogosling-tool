import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import { VIZ_BACKEND_URL } from './Config';
import './App.css';
import {GoslingEditorPre, DEFAULT_SPEC} from './GoslingEditorPre';
// import {GoslingComponent} from "gosling.js";
import {EX_SPEC_BASIC_SEMANTIC_ZOOM} from "./default_specs";



function DataResult({ data } : {data : any}) {
  const { labelled_image, shape_image, property_image, spec, ...rest } = data
  return (
    <div>
      <h3>Viz Analysis Results</h3>
      <h6>Labelled Image (from JSON)</h6>
      <img src={labelled_image} />
      <h6>YoloV7's predictions of the charts' shape</h6>
      <img src={shape_image} />
      <h6>YoloV7's predictions of the chart's type</h6>
      <img src={property_image} />
      <GoslingEditorPre spec={JSON.stringify(spec)}/>
      <pre>{JSON.stringify(rest, null, 2)}</pre>
    </div>)
}
function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState()
  const [error, setError] = useState(false)
  // const gosRef = React.useRef(null)
  const handleSubmit = async (e: any) => {
    e.preventDefault()
    const formObject = new FormData(e.currentTarget)
    // alert("submitting!")
    const response = await fetch(VIZ_BACKEND_URL, {
      method: "POST",
      body: formObject
    })
    const json = await response.json()
    setData(json)
    setError(!response.ok)
    setHasData(true)
  }
  

  return (
    <div className="App">
      <h1>Autogosling Frontend</h1>
      <p>Upload your image here:</p>
      <form onSubmit={handleSubmit}>
        <input type="file" name="image" id="image" />
        {/* <input type="file" name="json" id="image" /> */}
        <button type="submit">Submit image</button>
      </form>
      <br />
      {(hasData && !error) && <DataResult data={data} />}
      {(hasData && !error) &&<GoslingEditorPre spec={DEFAULT_SPEC}/>}
    </div>
  );
}

export default App;
