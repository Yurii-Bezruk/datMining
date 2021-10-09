import java.awt.Color;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.Border;


public final class ApplicationFrame extends JFrame {
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;

	private JFileChooser fileChooser;
	
	private JTextField fileTextField;
	private JButton openFileButton;
	private JScrollPane scrollPane;
	private JTextArea messageArea;
	private JButton checkButton;
	
	public ApplicationFrame() {
		setTitle("Bayesian naive classifier");
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setBounds(150, 150, 550, 350);		
		contentPane = new JPanel();
		
		GridBagLayout layout = new GridBagLayout();
		GridBagConstraints constraints = new GridBagConstraints();

		contentPane.setLayout(layout);

		constraints.anchor = GridBagConstraints.CENTER; 
		constraints.fill = GridBagConstraints.NONE;  
		constraints.gridheight = 1;
		constraints.gridwidth = 1; 
		constraints.gridx = 0; 
		constraints.gridy = 0; 
		constraints.insets = new Insets(0, 0, 0, 0);
		constraints.ipadx = 0;
		constraints.ipady = 0;
		constraints.weightx = 1;
		constraints.weighty = 1;
		
		
		setContentPane(contentPane);
				
		fileChooser = new JFileChooser(new File(System.getProperty("user.dir")));
		Border border = BorderFactory.createLineBorder(Color.GRAY);
		
		JLabel fileLabel = new JLabel("Choose learning file: ");
		constraints.gridwidth = 2;
		layout.setConstraints(fileLabel, constraints);
		contentPane.add(fileLabel);
		constraints.gridwidth = 1;
		constraints.gridx = 0; 
		constraints.gridy = 1; 
		fileTextField = new JTextField(30);
		fileTextField.setBorder(border);
		layout.setConstraints(fileTextField, constraints);
		contentPane.add(fileTextField);
		constraints.gridx = 1; 
		openFileButton = new JButton("Open Learning file");
		openFileButton.setFocusable(false);
		openFileButton.addActionListener(event -> {
			int result = fileChooser.showOpenDialog(this);
			if (result == JFileChooser.APPROVE_OPTION)
                fileTextField.setText(fileChooser.getSelectedFile().getAbsolutePath());
		});
		layout.setConstraints(openFileButton, constraints);
		contentPane.add(openFileButton);
		
		JLabel messageLabel = new JLabel("Enter testing message: ");
		constraints.gridwidth = 2;
		constraints.gridx = 0; 
		constraints.gridy = 2; 
		layout.setConstraints(messageLabel, constraints);
		contentPane.add(messageLabel);
		constraints.gridx = 0; 
		constraints.gridy = 3; 
		messageArea = new JTextArea(10, 40);
		messageArea.setBorder(border);
		scrollPane = new JScrollPane(messageArea, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
		layout.setConstraints(scrollPane, constraints);
		contentPane.add(scrollPane);
		constraints.gridx = 0; 
		constraints.gridy = 4;
		checkButton = new JButton("Check");
		checkButton.addActionListener(new CheckButtonListener());
		layout.setConstraints(checkButton, constraints);
		contentPane.add(checkButton);		
		setVisible(true);
	}
	
	private class CheckButtonListener implements ActionListener{
		
		@Override
		public void actionPerformed(ActionEvent event) {
			try {
				String filename = fileTextField.getText();
				String message =  messageArea.getText().replaceAll("\"", " ");
				if(filename.equals("") || message.equals("")) {
					JOptionPane.showMessageDialog(ApplicationFrame.this, "Invalid Input!");
					return;
				}
		        Runtime runtime = Runtime.getRuntime();
		        System.out.println(filename);
		        Process process = runtime.exec(String.format("py bayesian_classifier.py --file \"%s\" --message \"%s\"", filename, message));
		        BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));
		        BufferedReader error = new BufferedReader(new InputStreamReader(process.getErrorStream()));
		        List<String> output = new ArrayList<>();
		        List<String> stackTrace = new ArrayList<>();
		        String next = null;
		        while((next = input.readLine()) != null) {
					output.add(next);
				}
		        while((next = error.readLine()) != null) {
		        	stackTrace.add(next);
				}

		        int exitVal = process.waitFor();
		        if(exitVal != 0) {
		        	for (String string : stackTrace) {
						System.err.println(string);
					}
		        	JOptionPane.showMessageDialog(ApplicationFrame.this, "Error during evaluation!");
		        }
		        else {
		            double spam = Double.parseDouble(output.get(0));
		            double ham = Double.parseDouble(output.get(1));
		            JOptionPane.showMessageDialog(ApplicationFrame.this,
		                String.format("Spam probability: %.4f%%%n Ham probability: %.4f%%%n Conclusion: It is %s",
		                    spam,
		                    ham,
		                    spam > ham ? "spam" : "ham"
		                )
		            );
		        }
		        System.out.println("Exited with error code "+exitVal);
		    } catch(Exception e) {
		    	e.printStackTrace();
		    }
			
		}
	}
	
	public static void main(String[] args) {
		new ApplicationFrame();
	}
}
