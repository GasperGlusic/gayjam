using UnityEngine;
using Unity.Random;

public class  : MonoBehaviour
{
   int i, je = 0;
   public float cas;

    void Detonacija() {
        i = Random.Range(1, 3);
        if(i == 1) {
            //.. tu se duplicirajo
        }
    }

    void Update() {
        if(je == 0) {
            je = 1;
            Invoke("Detonacija", cas);
        }
    }

}

