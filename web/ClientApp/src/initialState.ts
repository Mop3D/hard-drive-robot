import { ApplicationState } from "./store";

// Get the application-wide store instance, prepopulating with state from the server where available.
const initialState = ({
  disk: {
    isLoading: false,
    error: false,
    data: {
      diskid: "",
      mountpoints: []
    }
  }
} as unknown) as ApplicationState;

export default initialState;
