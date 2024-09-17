import { Mutex } from 'async-mutex'
import { fetchBaseQuery } from "@reduxjs/toolkit/query"


const reauthMutex = new Mutex()


export const createBaseQuery = (baseQueryArgs) => {
    const baseQuery = fetchBaseQuery({
        prepareHeaders: (headers) => headers,
        ...baseQueryArgs,
    })

    const baseQueryWithReauth = async (args, api, extraOptions) => {
        await reauthMutex.waitForUnlock()
        let result = await baseQuery(args, api, extraOptions)
        if (result.error) {
            if (result.error.status === 401) {
                await reauthMutex.waitForUnlock()
                result = await baseQuery(args, api, extraOptions)
            }
        }
        return result
    }

    return baseQueryWithReauth
}