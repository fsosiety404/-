using System;
using System.IO;

class Program
{
    static void Main()
    {

        while (true)
        { 
            //предоставляем выбор между чтением содержимого другого файла в файл посредник между питоном и просто записи в консоль
            Console.Write("Select position read text for file or text(1 or 2):   ");
            string select = Console.ReadLine();
            //если выбор 1 то тогда читаем из друого файла и записыаем в основной
            if (select == "1")
            {
                Console.Write("Please enter name file: ");
                string filename = Console.ReadLine();
                
                //определяем юзера
                string user_name = Environment.UserName;
                
                //дефолтное значение
                string pyt_file = "";

                string pyt_to_osn_file = "";
                

                if (OperatingSystem.IsLinux())
                {
                    //сстовляем путь
                    pyt_file = $"/home/{user_name}/{filename}";
                }

                if (OperatingSystem.IsWindows())
                {
                    pyt_file = $"C:\\Users\\{user_name}\\Desktop\\{filename}";
                }
                
                //проверка на существование файла

                if (File.Exists(pyt_file))
                {
                    Console.WriteLine();
                
                    Console.WriteLine("Read text from file...: ");
                
                    //читаем текст
                    string read_other_file = File.ReadAllText(pyt_file);
                
                    Console.WriteLine();
                    Console.WriteLine("read success! ");

                    if (OperatingSystem.IsLinux())
                    {
                        //состовляем путь до основного файла
                        pyt_to_osn_file = $"/home/{user_name}/file_python_cs.txt";
                    }

                    if (OperatingSystem.IsWindows())
                    {
                        pyt_to_osn_file = $"C:\\Users\\{user_name}\\Desktop\\file_python_cs.txt";
                    }
                
                    //записываем
                    File.WriteAllText(pyt_to_osn_file, read_other_file);
                
                    //сообщаем что успешно 
                    Console.WriteLine("write success! run the python file and reload server to apply changes");
                
                    Console.Write("Press any key to exit...");
                    Console.ReadKey();
                }

                else
                {
                    Console.Write("error: file not found");
                }
            }

            if (select == "2")
            {
                Console.Write("Please enter text: ");
                string text = Console.ReadLine();

                //определяем юзера
                string user_name2 = Environment.UserName;

                //состовляем путь до основного файла
                string pyt_to_osn_file2 = $"/home/{user_name2}/file_python_cs.txt";

                //записываем
                File.WriteAllText(pyt_to_osn_file2, text);

                //сообщаем об успешной записи
                Console.WriteLine("write success! run the python file and reload server to apply changes");

                Console.Write("Press any key to exit...");
                Console.ReadKey();
                Console.WriteLine();
            }
            
            else
            {
                Console.WriteLine("error: choice the right position");
            }

        }
    }
}