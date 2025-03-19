using System;
using System.Collections.Generic;

[Serializable] 
public class ConfusionData
{
    public float confusion { get; set; }
    public List<string> confusing_topics { get; set; }

    public ConfusionData()
    {
        confusion = 0;
        confusing_topics = new List<string>();
    }
}