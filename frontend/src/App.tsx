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
import { PredictionTable } from './GoslingTable';

const UploadImageComponent = ({ handleFile } : {handleFile : any}) => (
  <Box className="setup">
    <Box className="uploadBox" sx={{ width: '100%' }}>
      <form>
        <Button variant="contained" component="label">Choose image to analyze
          <input type="file" name="image" id="image" hidden onChange={handleFile} />
        </Button>
      </form>
    </Box>
  </Box>
)
function AppStepper({ data, step, handleFile, showData }: { data: any, handleFile : any, step: any, showData : any }) {
  debugger 
  const initialTracksInfo = !!data ? data.tracks_info : []
  const [currentTracksInfo, setCurrentTracksInfo] = useState(initialTracksInfo)
  useEffect(() => {
    setCurrentTracksInfo(initialTracksInfo)
  },[data])
  if (!showData){
    return <UploadImageComponent handleFile={handleFile}/>
  }
  const { tracks_info: tracksInfo, image, width, height } = data
  const predictionComponent = (<div>
    <GoslingSketch image={image} tracksInfo={currentTracksInfo} width={width} height={height} />
    <PredictionTable currentTracksInfo={currentTracksInfo} setCurrentTracksInfo={setCurrentTracksInfo}></PredictionTable>
  </div>)
  const editorComponent = !!data.spec ? <GoslingEditorPre spec={JSON.stringify(data.spec)} /> : <div>AutoGosling could not generate a spec file as there was nothing detected.</div>;
  // alert('hi')
  const componentArray = [<UploadImageComponent handleFile={handleFile}/>, predictionComponent, editorComponent]
  return componentArray[step]

}

function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState()
  const [error, setError] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  const handleFile = async (e: any) => {
    const formObject = new FormData(e.target.form)
    console.log(formObject)
    const response = await fetch(VIZ_BACKEND_URL, {
      method: "POST",
      body: formObject
    })
    const json = await response.json()
    setData(json)
    setError(!response.ok)
    setHasData(true)
    setActiveStep(prev => prev + 1)
  }

  const handleNavigation = () => {
    setActiveStep((prevActiveStep) => Math.min(2,prevActiveStep+1));
  }
  const MAX_STEPS = 2
  return (
    <div className="App">
      <Typography>
        <h1 className="page-title">AutoGosling</h1>
      </Typography>
      <Box className="results" sx={{ width: '100%' }}>
        <Box sx={{ width: '100%' }}>
          <Stepper activeStep={activeStep}>
            <Step key={0}>
              <Typography>
                <StepLabel>Upload</StepLabel>
              </Typography>
            </Step>
            <Step key={1}>
              <Typography>
                <StepLabel>Detection</StepLabel>
              </Typography>
            </Step>
            <Step key={2}>
              <Typography>
                <StepLabel>Reconstruction</StepLabel>
              </Typography>
            </Step>
          </Stepper>

        </Box>
        <Box className="stepper-buttons">
          <Box style={{ flex: "1 1 auto" }} hidden={activeStep === 2}></Box>
          {activeStep != 0 &&
          <Button variant="contained" onClick={() => setActiveStep(prev => Math.max(prev -1,0))}>
            Back
          </Button>
          }
          {activeStep != MAX_STEPS && <Button variant="contained" onClick={() => setActiveStep(prev => Math.min(prev + 1,10))}>
            Next
          </Button>}
        </Box>
        <AppStepper showData={hasData && !error} data={data} step={activeStep} handleFile={handleFile}/>
      </Box>
    </div >
  );
}

export default App;
