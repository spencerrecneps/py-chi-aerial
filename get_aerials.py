from argparse import ArgumentParser
from urllib2 import urlopen, URLError
from math import ceil, floor
import os


def roundDown(val):
    '''
    Rounds the value down to the nearest 5,000
    '''
    f = val/5000
    r = floor(f)
    r = r*5000
    return int(r)

    
def roundUp(val):
    '''
    Rounds the value up to the nearest 5,000
    '''
    f = val/5000
    r = ceil(f)
    r = r*5000
    return int(r)

    
def main():
    # Parse command line args
    parser = ArgumentParser(description='Download aerial imagery for Chicagoland.')
    parser.add_argument("--left", type=int, help='X-coordinate of the westernmost point in the bounding box', dest="left", required=True)
    parser.add_argument("--bottom", type=int, help='Y-coordinate of the southernmost point in the bounding box', dest="bottom", required=True)
    parser.add_argument("--right", type=int, help='X-coordinate of the easternmost point in the bounding box', dest="right", required=True)
    parser.add_argument("--top", type=int, help='Y-coordinate of the northernmost point in the bounding box', dest="top", required=True)
    parser.add_argument("--directory", "-d", help='The directory location to store downloaded files', dest="dir", required=True)
    args = parser.parse_args()
    
    # Check that values fall within available aerial data and make sense
    if args.left > args.right:
        raise ValueError('The left value is greater than the right value')
    if args.bottom > args.top:
        raise ValueError('The bottom value is greater than the top value')
    if args.left < 880000:
        raise ValueError('The left value is outside of the available area')
    if args.right > 1205000:
        raise ValueError('The right value is outside of the available area')
    if args.bottom < 1650000:
        raise ValueError('The bottom value is outside of the available area')
    if args.top > 2120000:
        raise ValueError('The top value is outside of the available area')
    
    # Check that the directory exists or can be created
    if not os.path.exists(args.dir):
        try:
            os.mkdir(args.dir)
        except:
            raise OSError('Destination path %s does not exist and could not be created' % args.dir)
    
    # Get the normalized values (rounded to increments of 5,000)
    left = roundDown(args.left)
    bottom = roundDown(args.bottom)
    right = roundUp(args.right)
    top = roundUp(args.top)
    
    # Set base vars
    baseurl = "http://crystal.isgs.uiuc.edu/nsdihome/webdocs/cua05/data/cua2005spe_zip/"
    
    # Get the ranges
    if left==right:
        xrange = [left]
    else:
        xrange = range(left, right, 5000)
    if bottom==top:
        yrange = [top]
    else:
        yrange = range(bottom, top, 5000)
    
    # Loop through and download all files
    for x in xrange:
        for y in yrange:
            xname = str(x).zfill(7)
            yname = str(y).zfill(7)
            i = baseurl + xname + '/' + xname + '_' + yname + '.zip'
            o = os.path.join(args.dir,xname + '_' + yname + '.zip')
            print("retrieving " + i + ", saving to " + o + ")\n")
            
            # Download the file and save to the local destination
            try:
                f = urlopen(i)
                with open(o, "wb") as local:
                    local.write(f.read())
            except URLError:
                print "Could not find file at %s" % i
                
        
if __name__ == "__main__":
    main()