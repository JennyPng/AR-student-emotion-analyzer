// Unity Client (Unity C# Script - Attach to a GameObject)
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.Collections; // Install via Unity Package Manager: Newtonsoft Json

public class SocketClient : MonoBehaviour
{

    //public string serverIP = "10.18.156.162";
    //public string serverIP = "205.175.106.52"; // 
    public string serverIP = "172.20.10.3"; // MINE ON HOTSPOT

    //public string serverIP = "10.19.108.229"; // brians
    //public string serverIP = "172.20.10.2"; // brians on my hotspot

    public int serverPort = 65432;

    private TcpClient client;
    private NetworkStream stream;

    //private Thread clientReceiveThread;

    private bool isRunning;
    //private List<string> receivedTextList = new List<string>();

    private TextManager textManager;

    void Start()
    {
        textManager = TextManager.Instance;
        ConnectToServer();
    }

    void ConnectToServer()
    {
        try
        {
            client = new TcpClient(AddressFamily.InterNetwork);
            client.Connect(serverIP, serverPort);

            stream = client.GetStream();
            isRunning = true;

            StartCoroutine(ReceiveData());
            //clientReceiveThread = new Thread(new ThreadStart(ReceiveData));
            //clientReceiveThread.IsBackground = true;
            //clientReceiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.LogError("Socket error: " + e);
        }
    }

    IEnumerator ReceiveData()
    {
        byte[] receiveBuffer = new byte[1024];
        StringBuilder stringBuilder = new StringBuilder(); // Buffer for incomplete JSON

        while (isRunning)
        {
            try
            {
                int bytesRead = stream.Read(receiveBuffer, 0, receiveBuffer.Length);
                if (bytesRead > 0)
                {
                    string receivedData = Encoding.UTF8.GetString(receiveBuffer, 0, bytesRead);
                    stringBuilder.Append(receivedData);

                    string data = stringBuilder.ToString();

                    if (data.Contains("\n")) // Check for end of JSON
                    {
                        string[] jsonStrings = data.Split('\n', StringSplitOptions.RemoveEmptyEntries);
                        foreach (string jsonString in jsonStrings)
                        {

                            try
                            {
                                ConfusionData confusionData = JsonConvert.DeserializeObject<ConfusionData>(jsonString);

                                Debug.Log("received: " + confusionData.confusion.ToString());

                                if (confusionData != null)
                                {
                                    // Enqueue the update to run on the main thread
                                    //UnityMainThreadDispatcher.Enqueue(() => textManager.updateConfusionData(confusionData));
                                    textManager.updateConfusionData(confusionData);
                                }

                                stringBuilder.Clear(); // Clear the buffer
                            }
                            catch (JsonException e)
                            {
                                Debug.LogError("JSON parsing error: " + e);
                                // Handle the error, potentially by waiting for more data
                            }
                        }
                    }

                }
            }
            catch (SocketException socketException)
            {
                Debug.LogError("Socket exception: " + socketException);
                break;
            }
            catch (System.IO.IOException ioException)
            {
                Debug.LogError("IO exception: " + ioException);
                break;
            }
            catch (Exception e)
            {
                Debug.LogError("Receive error: " + e);
                break;
            }
        }
        yield return null;
    }

    //void OnApplicationQuit()
    //{
    //    isRunning = false;
    //    if (clientReceiveThread != null && clientReceiveThread.IsAlive)
    //    {
    //        clientReceiveThread.Join();
    //    }

    //    if (stream != null)
    //    {
    //        stream.Close();
    //    }
    //    if (client != null)
    //    {
    //        client.Close();
    //    }
    //}

    //public List<string> GetReceivedTextList()
    //{
    //    return receivedTextList;
    //}

    void Update()
    {

    }
}