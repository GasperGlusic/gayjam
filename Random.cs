using UnityEngine;
using Unity.Random;

public class  : MonoBehaviour
{
   int i, je = 0;
   public float cas, casD;
   public gameObject objekt;

    void Detonacija() {
        i = Random.Range(1, 3);
        if(i == 1) {
            //.. tu se duplicirajo
        }
    }

    void kloniranje()
    {
       Instantiate(objekt, gameObject.transform.position, Quaternion.identity);
       Destroy(objekt, casD);
    }

    void Update() {
        if(je == 0) {
            je = 1;
            Invoke("Detonacija", cas);
        }
    }

}

