using UnityEngine;
using TMPro;
using System.Linq;
using System.Text;
using static Oculus.Interaction.Context;
using System.Collections.Generic;

public class TextManager : MonoBehaviour
{
    public static TextManager Instance;

    public TextMeshProUGUI feedbackText;
    public TextMeshProUGUI confusionText;

    public ConfusionData confusionData;
    private bool notify;
    private float notifyStart;

    private static string NO_CONFUSION = "No confusing topics yet!";

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this; 
            DontDestroyOnLoad(gameObject); 
        }
        else
        {
            Destroy(gameObject);  
        }
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        feedbackText.text = "No confusions so far!";
        notify = false;
        notifyStart = -1;
        confusionData = new ConfusionData(); 
        confusionText.text = confusionData.confusion.ToString();
    }

    public void updateConfusionData(ConfusionData newData)
    {
        Debug.Log("In updateConfusionData at " + Time.time.ToString());
        if (!newData.confusing_topics.SequenceEqual(confusionData.confusing_topics)) {
            Debug.Log("UNEQUAL");
            notify = true;
        }

        this.confusionData = newData;

        if (confusionData.confusing_topics.Count() == 0)
        {
            feedbackText.text = NO_CONFUSION;
        } else
        {
            StringBuilder sb = new StringBuilder();
            foreach (string s in confusionData.confusing_topics)
            {
                sb.Append("• " + s + "\n");
            }
            feedbackText.text = sb.ToString();
        }
        confusionText.text = confusionData.confusion.ToString();
    }

    // Update is called once per frame
    void Update()
    {
        // display notification icon if confusing topics has changed
        if (notify) {
            Debug.Log("NOTIFICATION");
            if (notifyStart == -1)
            {
                notifyStart = Time.time;
            } else if (Time.time - notifyStart == 5)
            {
                Debug.Log("hide notification");
                notify = false;
            }
        }   
    }
}
