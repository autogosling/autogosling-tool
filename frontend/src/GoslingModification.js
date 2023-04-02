import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { GoslingEditorPre, DEFAULT_SPEC,stripJsonComments } from './GoslingEditorPre';


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function BasicTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
          <Tab label="Gosling.js" {...a11yProps(0)} />
          <Tab label="GosTalk" {...a11yProps(1)} />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        Gosling.js
      </TabPanel>
      <TabPanel value={value} index={1}>
        GosTalk
      </TabPanel>
    </Box>
  );
}


class GoslingModification extends React.Component{
  constructor(prop){
    super(prop);
    console.log(this.props.spec)
    this.state = {
      spec: this.props.spec
    }
  }

  render(){
    console.log(this.state.spec)
    return (
      <div>
        <GoslingEditorPre spec={JSON.stringify(this.state.spec)} />
      </div>
    )
  }
}

export { GoslingModification };