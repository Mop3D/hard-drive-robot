// functions
export const robopiApi = (callname: string) => {
  const robopiapiurl = "http://debian-2:8888/api";
  switch (callname)
  {
    case "ping":
      return robopiapiurl + "/ping?dast=true";
      break;
  }
  return ""
};
export const robopiWs = () => {
  return "ws://debian-2:8888/ws";
}

