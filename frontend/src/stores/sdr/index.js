import { createApi } from '@reduxjs/toolkit/query/react'
import {createBaseQuery} from "../createBaseQuery.js";
import {BACKEND_DOMAIN} from "../constants.js";

export const sdrApi = createApi({
    reducerPath: 'sdr',
    baseQuery: createBaseQuery({ baseUrl: `http://${BACKEND_DOMAIN}` }),
    tagTypes: ['sdr'],
    endpoints: (builder) => ({
        setCenterFreq: builder.mutation({
            query: (centerFreq) => ({
                url: `/sdr/set_center_freq?center_freq_m=${centerFreq}`,
                method: 'POST',
            }),
            invalidatesTags: ['sdr'],
        }),
        saveFile: builder.mutation({
            query: (class_name) => ({
                url: `/sdr/write_file?class_name=${class_name}`,
                method: 'POST',
            }),
            invalidatesTags: ['sdr'],
        }),
    }),
})

export const {
    useSetCenterFreqMutation,
    useSaveFileMutation,
} = sdrApi
