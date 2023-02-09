using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.UI;
using NetMQ;
using NetMQ.Sockets;
using System.Linq;
using System;
using System.IO;
using System.IO.Compression;
using Newtonsoft.Json;

public class CameraScript : MonoBehaviour
{

    int currentCamIndex = 0;

    WebCamTexture tex;

    public RawImage display;

    public Text startStopText;

    // ZeroMQ socket for sending data
    PublisherSocket socket;

    void Start()
    {
        // create a ZeroMQ socket and bind it to the specifed endpoint\
        socket = new PublisherSocket();
        socket.Bind("tcp://*:5555");

    }



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
            Console.WriteLine("Hello World!");
        }
        else // Start the Camera
        {
            WebCamDevice device = WebCamTexture.devices[currentCamIndex];
            tex = new WebCamTexture(device.name);
            display.texture = tex;

            // start the camera
            tex.Play();

            Debug.Log("Camera Started");

            startStopText.text = "Stop Camera";
        }
    }

    public void Update()
    {

        Debug.Log("Update");
        // System.Threading.Thread.Sleep(3);

        if (tex != null)
        {
            // Convert the webcam data to a byte array andf send it using the ZeroMQ socket
            Color32[] pixels = tex.GetPixels32();
            // load the pixels into a byte array
            byte[] buffer = new byte[pixels.Length * 4];

            for (int i = 0; i < pixels.Length; i++)
            {
                Color32 c = pixels[i];
                buffer[i * 4] = c.r;
                buffer[i * 4 + 1] = c.g;
                buffer[i * 4 + 2] = c.b;
                buffer[i * 4 + 3] = c.a;
            }


            Debug.Log(buffer.Length);

            using (MemoryStream ms = new MemoryStream())
            {
                using (GZipStream gzip = new GZipStream(ms, CompressionMode.Compress))
                {
                    gzip.Write(buffer, 0, buffer.Length);
                }
                byte[] compressedImageData = ms.ToArray();

                socket.SendFrame(compressedImageData);
            }

            Debug.Log("Sent data" + buffer.Length);

        }
    }

    private void StopWebcam()
    {
        display.texture = null;
        tex.Stop();
        tex = null;
    }

    private void OnDestroy()
    {
        socket.Dispose();
    }

}
