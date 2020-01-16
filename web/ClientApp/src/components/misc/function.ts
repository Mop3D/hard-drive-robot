// functions
export const robopiApi = (callname: string) => {
  const robopiapiurl = "http://hdrobo:8888";
  console.log("call api", callname)
  switch (callname)
  {
    case "ping":
      return robopiapiurl + "/api/ping?dast=true";
      break;
    default:
      return robopiapiurl + callname;
      break;
  }
  return ""
};
export const robopiWs = () => {
  return "ws://hdrobo:8888/ws";
}

