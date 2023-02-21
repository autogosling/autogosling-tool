import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import { GROUND_VIZ_BACKEND_URL, VIZ_BACKEND_URL } from './Config';
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
  const initialSpec = !!data ? data.spec : []
  const [spec,setSpec] = useState(initialSpec)
  const [currentTracksInfo, setCurrentTracksInfo] = useState(initialTracksInfo)
  const [confirmed, setConfirmed] = useState(false);
  useEffect(() => {
    setCurrentTracksInfo(initialTracksInfo)
  },[data])
  if (!showData){
    return <UploadImageComponent handleFile={handleFile}/>
  }
  if (JSON.stringify(data) === "{}"){
    return <div>AutoGosling could not find the ground truth in the dataset</div>
  }
  const { tracks_info: tracksInfo, image, width, height} = data
  const submitTable = async () =>{
    console.log("Submit table")
    const formObject = new FormData();
    formObject.append("predict", "False")
    formObject.append("track_info", JSON.stringify(currentTracksInfo))
    const response = await fetch(VIZ_BACKEND_URL, {
        method: "POST",
        body: formObject
      })
    const json = await response.json()
    if (json["spec"] != null){
      console.log(json["spec"])
      setSpec(json["spec"])
      if (!confirmed){
        setConfirmed(true);
      }
    }
    console.log("Json", json)
    
  }
  const predictionComponent = (<div>
    <GoslingSketch image={image} tracksInfo={currentTracksInfo} width={width} height={height} />
    <PredictionTable currentTracksInfo={currentTracksInfo} setCurrentTracksInfo={setCurrentTracksInfo}></PredictionTable>
    <Button onClick={() => submitTable()}>Confirm</Button>
    {/* {confirmed && <p>Changes have been saved!</p> } -->*/}
  </div>)
  const editorComponent = !!data.spec ? <GoslingEditorPre spec={JSON.stringify(spec)} /> : <div>AutoGosling could not generate a spec file as there was nothing detected.</div>;
  // alert('hi')
  const componentArray = [<UploadImageComponent handleFile={handleFile}/>, predictionComponent, editorComponent]
  return componentArray[step]

}

function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState()
  const [error, setError] = useState(false)
  const [useGround, setUseGround] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  const handleFile = async (e: any) => {
    const formObject = new FormData(e.target.form)
    formObject.append("predict", "True")
    console.log(formObject)
    const response = await fetch(useGround ? GROUND_VIZ_BACKEND_URL : VIZ_BACKEND_URL, {
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
        <Button variant="outlined" onClick={() => setUseGround(prev => !prev)}>{useGround ? "Currently showing Ground Truth. Click to show predictions" : "Currently showing predictions. Click to show ground truth"}</Button>
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
          {activeStep != MAX_STEPS && <Button variant="contained" onClick={() => { 
            setActiveStep(prev => Math.min(prev + 1,10))
          }}>
            Next
          </Button>}
        </Box>
        <AppStepper showData={hasData && !error} data={data} step={activeStep} handleFile={handleFile}/>
      </Box>
    </div >
  );
}

export default App;
