using UnityEngine;

public class  : MonoBehaviour
{
   void OnTriggerStay2D(Collider2D other)
    {
       if(other.CompareTag("Player")) {
        //koda se izvede tu..
       }
    }
}