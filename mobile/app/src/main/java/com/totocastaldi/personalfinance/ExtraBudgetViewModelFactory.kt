package com.totocastaldi.personalfinance

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.totocastaldi.personalfinance.repository.Repository

class ExtraBudgetViewModelFactory(private val repository: Repository): ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
         return ExtraBudgetViewModel(repository) as T
    }
}