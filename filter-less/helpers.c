#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            float red = image[i][j].rgbtRed;
            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            int l = round((red + blue + green) / 3);
            image[i][j].rgbtRed = l;
            image[i][j].rgbtBlue = l;
            image[i][j].rgbtGreen = l;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            float q = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            float p = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            float v = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if ( q > 255)
            {
                q = 255;
            }
            if ( p > 255)
            {
                p = 255;
            }
            if ( v > 255)
            {
                v = 255;
            }
            image[i][j].rgbtRed = q;
            image[i][j].rgbtGreen = p;
            image[i][j].rgbtBlue = v;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
           RGBTRIPLE k = image[i][j];
           image[i][j] =  image[i][width - (j+1)];
           image[i][width - (j+1)] = k;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            float counter = 0.00;
    int totalred = 0;
    int totalblue = 0;
    int totalgreen = 0;
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int currentx = i+x;
                    int currenty = j+y;
                    if(currentx > (height-1) || currenty > (width-1) || currentx < 0 || currenty < 0)
                    {
                        continue;
                    }
                    totalred = image[currentx][currenty].rgbtRed + totalred;
                    totalblue = image[currentx][currenty].rgbtBlue+ totalblue ;
                    totalgreen = image[currentx][currenty].rgbtGreen + totalgreen;
                    counter++;
            }
                    temp[i][j].rgbtRed = round(totalred/counter);
                    temp[i][j].rgbtGreen = round(totalgreen / counter);
                    temp[i][j].rgbtBlue = round(totalblue / counter);
        }
    }
    }
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
             image[i][j].rgbtGreen = temp[i][j].rgbtGreen ;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue ;
        }
    }
    return;
}
