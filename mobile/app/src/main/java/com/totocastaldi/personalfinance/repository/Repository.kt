package com.totocastaldi.personalfinance.repository

import com.totocastaldi.personalfinance.api.RetrofitInstance
import com.totocastaldi.personalfinance.model.Extra
import retrofit2.Response

class Repository {

    suspend fun getExtraBudget(idToken : String): Response<Extra> {
        return RetrofitInstance.api.getExtraBudget("31", "1643", listOf("Extra", "Svago"), idToken)
    }
}