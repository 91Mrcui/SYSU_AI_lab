
import classhead as ch
import funhead2 as fh
import tkinter as tk
import sys
#import datetime 


s=''
e=''

def run():
        
         #查看运行时间
        #starttime = datetime.datetime.now()
        global s,e
        global ip1,ip2
        '''mess=input("enter two city(enter 'q' to exit):")
        if mess=='q':
            break'''
            
        s=ip1.get()
        e=ip2.get()

        s=s.lower()
        e=e.lower()

        

        if len(s)==1 and s in rm.book3:
            s=rm.book3[s]
        if len(e)==1 and e in rm.book3:
            e=rm.book3[e]

        

        if s in rm.book and e in rm.book:
            sa,sb=fh.dj(rm,rm.book[s],rm.book[e])
            showmess.set(str(sa)+" : "+sb)

        else:
            showmess.set("Wrong!please enter correct cities.")


        #查看运行时间
        #endtime = datetime.datetime.now()
        #print((endtime - starttime))

def efun():
    sys.exit()

    

rm=ch.roman_map()
rm.read_message("Romania.txt")
    #---------------------------------------------------------------------
   
window=tk.Tk()
window.title('罗马尼亚旅行问题')
window.geometry('700x500')

show=tk.Label(window,text='Enter two cities:')
show.grid(row=1,column=1,padx=10, pady=10)
show_first=tk.Label(window,text='From:').grid(row=4, column=4, padx=10, pady=5)
show_second=tk.Label(window,text='To:').grid(row=5, column=4, padx=10, pady=5)
    
    #show_first.pack(padx=10, pady=20)
    #show_second.pack(padx=10, pady=40)
ip1=tk.Entry(window,show=None)
ip1.grid(row=4, column=5, padx=10, pady=5)
ip2=tk.Entry(window,show=None)
ip2.grid(row=5, column=5, padx=10, pady=5)
    #ip1.pack(padx=20, pady=20)
    #ip2.pack(padx=20, pady=40)

find_button=tk.Button(window,text='search',font=('Arial',10),width=7,height=1,command=run)
find_button.grid(row=6,column=4,padx=5, pady=5)

exit_button=tk.Button(window,text='exit',font=('Arial',10),width=7,height=1,command=efun)
exit_button.grid(row=6,column=5,padx=5, pady=5)


outmess=""

showmess=tk.StringVar()
showmess.set(outmess)
show=tk.Label(window,textvariable=showmess,font=('Arial',10))
show.grid(row=8,column=1,padx=20, pady=1)
    



    #---------------------------------------------------------------------
    
window.mainloop() 
