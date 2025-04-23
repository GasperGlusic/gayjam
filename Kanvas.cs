using UnityEngine;

public class Kanvas : MonoBehaviour
{
   public GameObject player;

   void Update() {
    gameObject.transform.position = player.transform.position;
   }
}
