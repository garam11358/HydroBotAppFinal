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
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.snackbar.Snackbar;

import org.opencv.android.OpenCVLoader;

import java.io.ByteArrayOutputStream;
import java.io.File;

public class ImageProcessing extends AppCompatActivity {

    String imageUriString;
    ConstraintLayout constraintLayout;
    ImageView ImageProcessingView;
    Button toImageCorrection;
    Bitmap imageBitmap;
    EditText newImageName;

    String baseDir;
    String picName;
    String FilePath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_processing);

        imageUriString = getIntent().getStringExtra("imageUri");
        Uri imageUri = Uri.parse(imageUriString);
        String imagePath = imageUri.getPath();

        baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
        newImageName = findViewById(R.id.newImageName);
        picName = newImageName.getText().toString();
        FilePath = baseDir + File.separator + picName + ".tiff";


        if(imagePath != null){
            if (!Python.isStarted()) {
                Python.start(new AndroidPlatform(ImageProcessing.this));
                pythonCode(imagePath, FilePath);
                imageBitmap = BitmapFactory.decodeFile(FilePath);
                ImageProcessingView = findViewById(R.id.imageGraphs);
                ImageProcessingView.setImageBitmap(imageBitmap);
            }
        }
        else{
            Snackbar.make(constraintLayout, "Please choose a image", Snackbar.LENGTH_INDEFINITE)
                    .setAction("Click to Go Back to Picture Importing", new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            Intent intent = new Intent(ImageProcessing.this, Picture_Importing.class);
                            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                            startActivity(intent);
                        }
                    }).show();

        }
        toImageCorrection = findViewById(R.id.ToImageCorrection);
        toImageCorrection.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Uri newImageURI = getImageUri(ImageProcessing.this, imageBitmap);
                String newImageURIString = newImageURI.toString();
                Intent intent = new Intent(ImageProcessing.this, image_correction.class);
                intent.putExtra("imageURI",newImageURIString);
                startActivity(intent);
            }
        });


    }

    protected void pythonCode(String imagePath, String newPicPath){
        Python py = Python.getInstance();
        PyObject imageProcFile = py.getModule("o1_Perspective_Transform.py");
        PyObject imagProc = imageProcFile.call(imagePath, newPicPath);
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