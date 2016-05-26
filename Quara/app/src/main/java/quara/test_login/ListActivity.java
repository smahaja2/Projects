package quara.test_login;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class ListActivity extends AppCompatActivity implements View.OnClickListener{

    public class Description{
        String name;
        String description;
        String comments;
        Description(String name, String description, String comments){
            this.name = name;
            this.description = description;
            this.comments = comments;
        }

        String getName()
        {
            return this.name;
        }

        String getDescription()
        {
            return this.description;
        }

    }

    private class MyListAdapter extends ArrayAdapter<Description>{
        ArrayList<Description> des;

        public MyListAdapter(ArrayList<Description> descriptions){
            super(ListActivity.this, R.layout.item_view, descriptions);
            this.des = descriptions;
        };

        @Override
        public View getView(int position, View convertView, ViewGroup parent)
        {
            View itemView = convertView;
            if (itemView == null)
            {
                itemView = getLayoutInflater().inflate(R.layout.item_view, parent, false);
            }

            Description DesCurr = this.des.get(position);

            TextView makeTitle = (TextView) itemView.findViewById(R.id.Title);
            makeTitle.setText(DesCurr.getName());

            TextView makesubTitle = (TextView) itemView.findViewById(R.id.subTitle);
            makesubTitle.setText(DesCurr.getDescription());

            return itemView;
        }


    }

    final Activity act = this;
    static Context tt;
    final Context temp = this;
    public static LinearLayout lyout1;
    public static LinearLayout lyout2;

    Button add;
    Button delete;

    EditText text1;
    EditText text2;
    EditText notesText;
    String selected;

    Context context1;
    String regId;
    ShareExternalServer appUtil;
    AsyncTask<Void, Void, String> shareRegidTask;

    final String MODIFY_QUEUE_STRING = "Modify Queue";

    // Keeps track of names that are already in the queue. Prevents user from submitting more than one quests.
    Map<String, Boolean> names_on_queue = new HashMap<String, Boolean>();

    UserLocalStore userLocalStore;

    Context context;

    public EditText createEditText(String hint)
    {
        EditText text = new EditText(temp);
        text.setLayoutParams(new AbsListView.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        text.setHint(hint);
        return text;
    }

    public void setView()
    {
        LinearLayout layout = (LinearLayout) findViewById(R.id.user_info_form);
        lyout1 = layout;
        layout.removeAllViews();
        LinearLayout linearLayout = (LinearLayout) findViewById(R.id.couse_student_form);
        lyout2 = linearLayout;
        linearLayout.removeAllViews();
        Intent intent = new Intent(temp, MyReceiverAdd.class);
        intent.setAction("com.pycitup.BroadcastReceiverAdd");
        sendBroadcast(intent);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        selected = MainActivity.selected;
        Question selected_queue = new Question("","","",selected);
        ServerRequests serverRequests = new ServerRequests(temp);
        List<String> name_list = new ArrayList<String>();
        final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, name_list);
        serverRequests.getQueueInBackground(selected_queue, new GetQueueCallBack() {
            @Override
            public void done(ArrayList returnQueue) {
                Iterator<ArrayList> iterator = returnQueue.iterator();
                ArrayList<Description> name_list = new ArrayList<Description>();
                ListView listview = (ListView) findViewById(R.id.listView);
                while (iterator.hasNext()) {
                    Map entry = (Map) iterator.next();
                    Description tv;
                    Map result = entry;
                    if (!result.get("user_notes").equals(""))
                        tv = new Description(result.get("user_name").toString(), "position: " + result.get("user_pos") + " topic: " + result.get("user_topic"), "notes: " + result.get("user_notes"));
                    else
                        tv = new Description(result.get("user_name").toString(), "position: " + result.get("user_pos") + " topic: " + result.get("user_topic"), "");
                    name_list.add(tv);
                }
                ArrayAdapter<Description> adapter = new MyListAdapter(name_list);
                listview.setAdapter(adapter);
            }
        });

        add = (Button) findViewById(R.id.add);
        add.setOnClickListener(this);

        delete = (Button) findViewById(R.id.delete);
        delete.setOnClickListener(this);
    }

    @Override
    public void onStart()
    {
        super.onStart();
    }

    public void onClick(View v) {
        switch(v.getId())
        {
            case R.id.add:
                //get text of add button
                final Button addButton = (Button)v;
                String buttonText = addButton.getText().toString();
                final boolean edit = buttonText == MODIFY_QUEUE_STRING;

                tt = temp;
                LinearLayout layout = (LinearLayout) findViewById(R.id.user_info_form);
                layout.removeAllViews();

                text1 = createEditText("Location");
                layout.addView(text1);

                text2 = createEditText("Topic");
                layout.addView(text2);

                notesText = createEditText("Comment");
                layout.addView(notesText);

                //create new submit button
                Button b = new Button(temp);
                if (edit) {
                    b.setText("edit");
                }
                else {
                    b.setText("submit");
                }
                b.setOnClickListener(
                        new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                String name = userLocalStore.getLoggedInUser().name;
                                LinearLayout layout = (LinearLayout) findViewById(R.id.user_info_form);
                                lyout1 = layout;
                                String pos = text1.getText().toString();
                                String topic = text2.getText().toString();
                                String notes = notesText.getText().toString();
                                Question queue = new Question(name, pos, topic, selected, notes);
                                ServerRequests serverRequests = new ServerRequests(temp);

                                if (!edit) { //insert into queue

                                    names_on_queue.put(name, true);

                                    //change the add button
                                    // text
                                    addButton.setText(MODIFY_QUEUE_STRING);

                                    serverRequests.insertQueueInBackground(queue, new GetQueueCallBack() {
                                        @Override
                                        public void done(ArrayList returnQueue) {
                                            ListActivity.this.setView();
                                        }
                                    });
                                }
                                else { //edit queue
                                    serverRequests.editQueueInBackground(queue, new GetQueueCallBack() {
                                        @Override
                                        public void done(ArrayList returnQueue) {
                                            ListActivity.this.setView();
                                        }
                                    });

                                }
                            }
                        }
                );
                layout.addView(b);
                break;
            case R.id.delete:
                //Change the other button's text back to add
                Button button = (Button)findViewById(R.id.add);
                button.setText("Add to queue");

                tt = temp;
                // we remove the name if they remove themselves from the queue
                names_on_queue.remove(userLocalStore.getLoggedInUser().name);
                layout = (LinearLayout) findViewById(R.id.user_info_form);
                layout.removeAllViews();
                String name = userLocalStore.getLoggedInUser().name;
                Question queue = new Question(name,"","",selected);
                ServerRequests serverRequests = new ServerRequests(temp);
                serverRequests.deleteQueueInBackground(queue, new GetQueueCallBack() {
                    @Override
                    public void done(ArrayList returnQueue) {
                        LinearLayout layout = (LinearLayout) findViewById(R.id.user_info_form);
                        lyout1 = layout;
                        layout.removeAllViews();
                        LinearLayout linearLayout = (LinearLayout) findViewById(R.id.couse_student_form);
                        lyout2 = linearLayout;
                        linearLayout.removeAllViews();
                        Intent intent = new Intent(temp, MyReceiverDelete.class);
                        intent.setAction("com.pycitup.BroadcastReceiverDelete");
                        sendBroadcast(intent);
                    }
                });
                break;
        }
    }

}
