import {combineReducers} from "@reduxjs/toolkit";
import {sdrApi} from "./sdr/index.js";

const reducer = combineReducers({
    [sdrApi.reducerPath]: sdrApi.reducer,
})

export const rootReducer = (state, action) => {
    return reducer(state, action)
}
