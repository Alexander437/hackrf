import {configureStore} from "@reduxjs/toolkit";
import {rootReducer} from "./reducers.js";
import {sdrApi} from "./sdr/index.js";
import {setupListeners} from "@reduxjs/toolkit/query";
import {useDispatch, useSelector} from "react-redux";

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
        }).concat([sdrApi.middleware]),
    devTools: false
})

setupListeners(store.dispatch)

export const useAppDispatch = () => useDispatch()
export const useAppSelector = useSelector