using System;

[Serializable] 
public class ConfusionData
{
    public float confusion;
    public string[] confusing_topics;

    public ConfusionData(float confusion, string[] confusingTopics)
    {
        this.confusion = confusion;
        this.confusing_topics = confusingTopics;
    }
    public ConfusionData()
    {
    }
}