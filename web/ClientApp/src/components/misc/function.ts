import axios from 'axios';
import { stringify } from 'querystring';

// const
// HDRobo HostName
export const HDRoboHostName = () => {
  return "hdrobo:8888";
}
// geht nicht?!?!?
export const HDRoboWS = () => {
  //const hdRoboWs = "ws://" + HDRoboHostName + "/ws"
  const hdRoboWsA = "ws://hdrobo:8888/ws"
  console.log("hdRoboWs", hdRoboWsA)
  return hdRoboWsA;
}

// functions

//
// send Command
//
export const SendCommand = async (stateObject: any, command: string, value?: number) => {
  var apiUrl = "";
  var motorName = "";
  var apiCommand = "";
  console.log("SendCommand", command)

  // common commands
  if (command === "ping")
  {
    apiUrl = "/api/ping?dast=true";
  }

  // motor commands
  if (apiUrl === "")
  {
    if (command === "up" || command === "down" || command === "slot" || command === "poweroff" || command === "reset" || command === "calibrate")
    {
        motorName = "Elevator";
    }
    if (command === "forward" || command === "backward" || command === "connect" || command === "release")
    {
        motorName = "Connector";
    }
    apiCommand = command;
    if (command === "up" || command === "down" || command === "forward" || command === "backward")
    {
      apiCommand = apiCommand + value;
    }
    if (command === "slot")
    {
      apiCommand = apiCommand + "?slotno=" + value;
    }
    if (motorName !== "")
      apiUrl = '/motor/' + motorName + "/" + apiCommand;
  }

  // nothing todo
  if (apiUrl === "")
  {
    return;
  }
  SendCommandToAPI(apiUrl, stateObject);
}


//
// send command to api
//
export const SendCommandToAPI = async (restUrl: string, stateObject: any) => {
      //const hdRoboApiUrl = "http://" + HDRoboHostName;
      const hdRoboApiUrl = "http://hdrobo:8888";
      const APIENDPOINT = hdRoboApiUrl + restUrl;
      console.log("sendAPICommand", APIENDPOINT)

      /* get dropdown data */
      const res = await axios.get(APIENDPOINT);
      const { data } = await res;
      try {
          console.log("sendAPICommand", restUrl, data)
          if (data) {
            stateObject.setState({
                  outMessage: "returnData: " + stringify(data),
                  hasError: false
              });
          } else {
              console.error("sendCommand - no valid data", data);
              stateObject.setState({ hasError: true });
          }
      } catch (e) {
          console.error("sendCommand - error data", e);
          stateObject.setState({ hasError: true });
      }
  }

