import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import { VIZ_BACKEND_URL } from './Config';
import './App.css';
import { GoslingEditorPre, DEFAULT_SPEC } from './GoslingEditorPre';
// import {GoslingComponent} from "gosling.js";
import GoslingSketch from "./GoslingSketch"
import { EX_SPEC_BASIC_SEMANTIC_ZOOM } from "./default_specs";
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
// import { PredictionTable } from './GoslingTable';

function DataResult({ data, step }: { data: any, step: Number }) {
  const { tracks_info: tracksInfo, image, spec, width, height } = data
  if (step === 0) {
    return <div>
      <GoslingSketch image={image} tracksInfo={tracksInfo} width={width} height={height} />
      {/*<PredictionTable tracksInfo={tracksInfo}></PredictionTable>*/}
      </div>
  }
  if (step === 1) {
    return <GoslingEditorPre spec={JSON.stringify(spec)} />;
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

  const handleFile = async (e: any) => {
    const formObject = new FormData(e.target.form)
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
      <Typography>
        <h1 className="page-title">AutoGosling</h1>
      </Typography>
      <Box className="setup">
        <Box className="uploadBox" sx={{ width: '100%' }}>
          <form>
            <Button variant="contained" component="label">Choose image to analyze
              <input type="file" name="image" id="image" hidden onChange={handleFile} />
            </Button>
          </form>
        </Box>
      </Box>
      {(hasData && !error) && <Box className="results" sx={{ width: '100%' }}>
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

        </Box>
        <Box className="stepper-buttons">
          <Box style={{flex: "1 1 auto"}} hidden={activeStep===1}></Box>
          <Button variant="contained" onClick={handleNavigation}>
            {activeStep === 1 ? 'Back' : 'Next'}
          </Button>
        </Box>
        <DataResult data={data} step={activeStep} />
      </Box>}
    </div >
  );
}

export default App;
