package com.garam.hydrobotappfinal;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.google.android.material.snackbar.Snackbar;
import com.opencsv.CSVWriter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class ImageGraphsActivity extends AppCompatActivity {

    String imageUriTG;
    Bitmap imageBitmap;
    ImageView imageGraphs;
    EditText newPicName3;

    ConstraintLayout constraintLayout;
    Button saveResults;

    String baseDir;
    String csvFileName;
    String FilePath;
    File csvFile;
    CSVWriter writer;
    FileWriter mFileWriter;

    String picName;
    String PicPath;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_image_graphs);

        imageUriTG = getIntent().getStringExtra("imageUri");
        Uri imageUri = Uri.parse(imageUriTG);
        String imagePath = imageUri.getPath();

        newPicName3 = findViewById(R.id.newImageName3);
        picName = newPicName3.getText().toString();
        PicPath = baseDir + File.separator + picName + ".tiff";

        baseDir = android.os.Environment.getExternalStorageDirectory().getAbsolutePath();
        csvFileName = picName + ".csv";
        FilePath = baseDir + File.separator + csvFileName;
        csvFile = new File(FilePath);


        if(imagePath != null){
            if(!Python.isStarted()){
                Python.start(new AndroidPlatform(ImageGraphsActivity.this));
                pythonCode(imagePath, PicPath);
                imageBitmap = BitmapFactory.decodeFile(PicPath);
                imageGraphs = findViewById(R.id.imageGraphs);
                imageGraphs.setImageBitmap(imageBitmap);
            }
        }else{
            Snackbar.make(constraintLayout, "Please choose a image", Snackbar.LENGTH_INDEFINITE)
                    .setAction("Click to Go Back to Picture Importing", new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            Intent intent = new Intent(ImageGraphsActivity.this, Picture_Importing.class);
                            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                            startActivity(intent);
                        }
                    }).show();
        }

        saveResults = findViewById(R.id.saveResults);
        saveResults.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(csvFile.exists() && csvFile.isDirectory()){
                    try {
                        mFileWriter = new FileWriter(FilePath, true);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    writer = new CSVWriter(mFileWriter);
                }else{
                    try {
                        writer = new CSVWriter(new FileWriter(FilePath));
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
                String[] headers = {"area", "equivalent diameter", "Perimeter", "Longest axis",
                        "Shortest axis", "Aspect Ratio"};

                writer.writeNext(headers);

                try {
                    writer.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

    }

    protected void pythonCode(String imagePath, String newPicPath){
        Python py = Python.getInstance();
        PyObject imageProcFile = py.getModule("o3_Shape_factor_extraction.py");
        PyObject imagProc = imageProcFile.call(imagePath, newPicPath);
    }
}