package com.totocastaldi.personalfinance

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.totocastaldi.personalfinance.model.Extra
import com.totocastaldi.personalfinance.repository.Repository
import kotlinx.coroutines.launch
import retrofit2.Response

class ExtraBudgetViewModel (private val repository : Repository) : ViewModel() {

    val myReposnse : MutableLiveData<Response<Extra>> = MutableLiveData()

    fun getExtraBudget(idToken : String) {
        viewModelScope.launch {
            val response = repository.getExtraBudget(idToken)
            myReposnse.value = response
        }
    }
}