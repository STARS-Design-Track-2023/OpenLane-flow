# STARS Openlane Wrapper

## Installation
```
git clone git@github.com:STARS-Design-Track-2023/OpenLane-flow.git
cd OpenLane-flow
./setup.py
```

If the install was successful you should see the following output in you terminal at the 
end of your run. You have sucessfullu set up your OpenLane environment!!
```
```
If you do not get the above output ***do not run the setup script again*** look at the 
common errors section. Once you have followed those instructions. Do the following
```
cd ~/OpenLane
make test
```
Hopefully now you see a successful test run.


## Common Error(s)

### 1) Environment variable is not recognized
If you get the following error.
```
```
please source your bashrc by doing the following
```
source ~/.bashrc
```
to test that it works
```
echo $PDK_ROOT
```
you should see the following
```
home/designer-XX/pdk
```

***If you see any other sort of errors other than the one(s) mentioned above please call a TA***
