import { ApplicationState } from "./..";

export const selectDisk = (state: ApplicationState) => {
    return state.disk.data;
};
