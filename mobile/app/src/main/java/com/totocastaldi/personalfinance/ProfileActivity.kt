package com.totocastaldi.personalfinance

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Parcelable
import android.util.Log
import androidx.appcompat.app.ActionBar
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.firebase.auth.FirebaseAuth
import com.totocastaldi.personalfinance.databinding.ActivityProfileBinding


class ProfileActivity : AppCompatActivity() {

    private lateinit var binding: ActivityProfileBinding

    private lateinit var actionBar: ActionBar

    private lateinit var firebaseAuth: FirebaseAuth

    private companion object {
        private const val TAG = "PROFILE"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityProfileBinding.inflate(layoutInflater)
        setContentView(binding.root)

        actionBar = supportActionBar!!
        actionBar.title = "Profile"

        firebaseAuth = FirebaseAuth.getInstance()

        checkUser()

        binding.logoutBtn.setOnClickListener {
            firebaseAuth.signOut()
            checkUser()
        }

        when {
            intent?.action == Intent.ACTION_SEND && intent.type?.startsWith("image/") == true -> {
                handleSendImage(intent)
            }
            else -> {
                Log.d(TAG, "action ${intent?.action}")
            }
        }
    }

    private fun handleSendImage(intent: Intent) {
        ActivityCompat.requestPermissions(
            this, arrayOf(
                android.Manifest.permission.READ_EXTERNAL_STORAGE,
                android.Manifest.permission.MANAGE_EXTERNAL_STORAGE
            ), 1
        )

        (intent.getParcelableExtra<Parcelable>(Intent.EXTRA_STREAM) as? Uri)?.let {
            Log.d(TAG, "$it")
            val uid = firebaseAuth.currentUser!!.uid
            UploadUtility(this).uploadFile(it, mapOf("uid" to uid, "type" to "image"))
        }
    }


    private fun checkUser() {
        var firebaseUser = firebaseAuth.currentUser
        if (firebaseUser != null) {
            val email = firebaseUser.email
            binding.emaulTv.text = email
        } else {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
}