package com.totocastaldi.personalfinance

import android.app.Activity
import android.app.ProgressDialog
import android.net.Uri
import android.util.Log
import android.webkit.MimeTypeMap
import android.widget.Toast
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

class UploadUtility(activity: Activity) {

    var activity = activity;
    var dialog: ProgressDialog? = null
    //var serverURL: String = "http://192.168.1.161:5000/file"
    //var serverURL: String = "https://personal-finance.toto-castaldi.com/api/file"
    var serverURL: String = "http://personal-finance.toto-castaldi.com:5000/file"

    val client = OkHttpClient()

    private companion object {
        private const val TAG = "UPLOAD"
    }

    fun uploadFile(sourceFileUri: Uri, dataParts: Map<String, String> ? = null) {
        val pathFromUri = URIPathHelper().getPath(activity, sourceFileUri)
        uploadFile(File(pathFromUri), dataParts)
    }

    fun uploadFile(sourceFile: File, dataParts: Map<String, String> ? = null) = Thread {
        val mimeType = getMimeType(sourceFile);
        if (mimeType == null) {
            Log.e("file error", "Not able to get mime type on sourceFile $sourceFile")
            return@Thread
        }
        val fileName: String = sourceFile.name
        toggleProgressDialog(true)
        try {
            var addFormDataPart = MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart(
                    "uploaded_file",
                    fileName,
                    sourceFile.asRequestBody(mimeType.toMediaTypeOrNull())
                )


            for ((k, v) in dataParts!!) {
                addFormDataPart = addFormDataPart.addFormDataPart(k, v)
            }

            val requestBody: RequestBody = addFormDataPart.build()

            val request: Request = Request.Builder().url(serverURL).post(requestBody).build()

            val response: Response = client.newCall(request).execute()

            if (response.isSuccessful) {
                Log.d(TAG,"success")
                showToast("File uploaded")
            } else {
                Log.e(TAG, "failed $response")
                showToast("File uploading failed $response")
            }
        } catch (ex: Exception) {
            ex.printStackTrace()
            Log.e("File upload", "failed")
            showToast("File uploading failed ${ex.message}")
        }
        toggleProgressDialog(false)
    }.start()

    // url = file path or whatever suitable URL you want.
    fun getMimeType(file: File): String? {
        var type: String? = null
        val extension = MimeTypeMap.getFileExtensionFromUrl(file.path)
        if (extension != null) {
            type = MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension)
        }
        return type
    }

    fun showToast(message: String) {
        activity.runOnUiThread {
            Toast.makeText( activity, message, Toast.LENGTH_LONG ).show()
        }
    }

    fun toggleProgressDialog(show: Boolean) {
        activity.runOnUiThread {
            if (show) {
                dialog = ProgressDialog.show(activity, "", "Uploading file...", true);
            } else {
                dialog?.dismiss();
            }
        }
    }

}