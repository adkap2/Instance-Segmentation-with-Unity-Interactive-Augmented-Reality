using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraScript : MonoBehaviour
{

    int currentCamIndex = 0;

    WebCamTexture tex;

    public RawImage display;

    public Text startStopText;

    private Texture2D tex2d;

    public Image CameraImage;

    public void SwapCam_Clicked()
    {
        
        if (WebCamTexture.devices.Length > 0)
        {
            currentCamIndex += 1;
            currentCamIndex %= WebCamTexture.devices.Length;

            // If tex is not null;
            // Stop the webcam
            // Start the webcam

            if (tex != null)
            {
                StopWebcam();
                StartStopCam_Clicked();
            }
        }

    }

    public void StartStopCam_Clicked()
    {

        if (tex != null) // Stop the Camera
        {
            StopWebcam();
            startStopText.text = "Start Camera";
        }
        else // Start the Camera
        {
            WebCamDevice device = WebCamTexture.devices[currentCamIndex];
            tex = new WebCamTexture(device.name);
            display.texture = tex;
            // start the camera
            tex.Play();
            tex2d = new Texture2D(tex.width, tex.height);
            CameraImage.material.mainTexture = tex2d;


            startStopText.text = "Stop Camera";


        }
    }

    public void Update()
    {
        if (tex.isPlaying)
        {
            var rawImage = text.GetPixels32();
            
        }
    }

    private void StopWebcam()
    {
        display.texture = null;
        tex.Stop();
        tex = null;
    }

}
