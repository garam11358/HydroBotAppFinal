package com.garam.hydrobotappfinal;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.snackbar.Snackbar;

import java.io.ByteArrayOutputStream;
import java.io.File;

public class image_correction extends AppCompatActivity {

    ImageView ImageCorrection;
    Button ToGraphs;
    String imageURIIC;
    ConstraintLayout constraintLayout;
    EditText threshold;
    Bitmap imageBitmap;
    EditText newPicName2;

    String baseDir;
    String picName;
    String FilePath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_correction);

        imageURIIC = getIntent().getStringExtra("imageURI");
        Uri imageUri = Uri.parse(imageURIIC);
        String imagePath = imageUri.getPath();

        threshold = findViewById(R.id.thresholdNum);
        String editTextString = threshold.getText().toString();
        int thresholdNum = Integer.parseInt(editTextString);

        baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
        newPicName2 = findViewById(R.id.newImageName2);
        picName = newPicName2.getText().toString();
        FilePath = baseDir + File.separator + picName + ".tiff";

        if(imagePath != null){
            if(!Python.isStarted()){
                Python.start(new AndroidPlatform(image_correction.this));
                pythonCode(imagePath, thresholdNum, FilePath);
                imageBitmap = BitmapFactory.decodeFile(FilePath);
                ImageCorrection = findViewById(R.id.imageGraphs);
                ImageCorrection.setImageBitmap(imageBitmap);
            }
        }else{
            Snackbar.make(constraintLayout, "Please choose a image", Snackbar.LENGTH_INDEFINITE)
                    .setAction("Click to Go Back to Picture Importing", new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            Intent intent = new Intent(image_correction.this, Picture_Importing.class);
                            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                            startActivity(intent);
                        }
                    }).show();
        }

        ToGraphs = findViewById(R.id.ToGraph);
        ToGraphs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Uri newImageUri = getImageUri(image_correction.this, imageBitmap);
                String newImageUriString = newImageUri.toString();
                Intent intent = new Intent(image_correction.this, ImageGraphsActivity.class);
                intent.putExtra("imageUri", newImageUriString);
                startActivity(intent);
            }
        });

    }

    protected void pythonCode(String imagePath, int threshold, String newPicPath){
        Python py = Python.getInstance();
        PyObject imageProcFile = py.getModule("o2_Image_correction.py");
        PyObject imagProc = imageProcFile.call(imagePath, threshold, newPicPath);
    }

    public Uri getImageUri(Context inContext, Bitmap inImage) {
        try {
            ByteArrayOutputStream bytes = new ByteArrayOutputStream();
            inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
            String path = MediaStore.Images.Media.insertImage(inContext.getContentResolver(), inImage, "Title", null);
            return Uri.parse(path);
        } catch (Exception e){
            e.printStackTrace();
            return null;
        }

    }
}