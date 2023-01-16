import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import { VIZ_BACKEND_URL } from './Config';
import './App.css';
import {GoslingEditorPre, DEFAULT_SPEC} from './GoslingEditorPre';
// import {GoslingComponent} from "gosling.js";
import GoslingSketch from "./GoslingSketch"
import {EX_SPEC_BASIC_SEMANTIC_ZOOM} from "./default_specs";
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

function DataResult({ data, step } : {data : any, step : Number}) {
  const {tracks_info : tracksInfo, image, spec, width, height} = data
  if (step === 0) {
    return       <GoslingSketch image={image} tracksInfo={tracksInfo} width={width} height={height}/>
  }
  if (step === 1) {
    return <GoslingEditorPre spec={JSON.stringify(spec)}/>;
  }
  return (
    <div>
      {/*<h2>YoloV7's predictions of the charts' shape</h2>*/}
      {/* <img src={image} /> */}
      <pre>{JSON.stringify(tracksInfo, null, 2)}</pre>
    </div>)
}
function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState()
  const [error, setError] = useState(false)
  const [activeStep, setActiveStep] = useState(0)
  
  
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
  
  const handleNavigation = () => {
    setActiveStep((prevActiveStep) => prevActiveStep === 0 ? 1 : 0);
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
      <Box sx={{ width: '100%' }}>
        <Stepper activeStep={activeStep}>

          <Step key={0}>
            <Typography>
              <StepLabel>Detection</StepLabel>
            </Typography>
          </Step>
          <Step key={1}>
          <Typography>
              <StepLabel>Reconstruction</StepLabel>
            </Typography>
          </Step>
        </Stepper>
        
        <Button onClick={handleNavigation}>
          {activeStep === 1 ? 'Back' : 'Next'}
        </Button>
      </Box>
      <br />
      {(hasData && !error) && <DataResult data={data} step={activeStep} />}
    </div>
  );
}

export default App;
